import sys
import os
import time
import json
import pandas as pd
from typing import Dict, List, Any
from tqdm import tqdm
from tabulate import tabulate
from dotenv import load_dotenv
from openai import OpenAI

# Setup path to import backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agent import LangGraphAgent
from backend.rag import ingest_file, init_collection

load_dotenv()

# Configuration
DATASET_PATH = os.path.join(os.path.dirname(__file__), "data", "rag_dataset_50.json")

# Point to the actual PDF
DUMMY_DOC_PATH = "/home/quang/My_Project/Document_Paraline/Agentic_RAG/backend/uploaded_files/Kinh_te_cong_nghiep.pdf" 
# Note: Variable name is kept as DUMMY_DOC_PATH to avoid refactoring the whole file, but it points to real data.
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "benchmark_results.csv")

class Benchmarker:
    def __init__(self):
        self.agent = LangGraphAgent()
        self.judge_client = OpenAI()
        
    def setup_data(self):
        """Pre-load necessary data for RAG tests."""
        print("Initializing Knowledge Base...")
        init_collection()
        print(f"Ingesting dummy policy from {DUMMY_DOC_PATH}...")
        try:
            ingest_file(DUMMY_DOC_PATH)
        except Exception as e:
            print(f"Warning during ingestion: {e}")

    def evaluate_response(self, question: str, expected: str, actual: str, trace: List[Dict]) -> Dict:
        """Use LLM-as-a-Judge to score the response."""
        
        prompt = f"""
        You are an impartial judge evaluating an AI Agent's performance.
        
        ### Context
        Question: {question}
        Expected Answer Ground Truth: {expected}
        Actual Agent Answer: {actual}
        Agent Execution Trace: {json.dumps(trace)}
        
        ### Evaluation Logic
        1. **Goal Achievement (1/0)**: Did the agent answer the core question?
        2. **Accuracy (1-5)**: How accurate is the information compared to the ground truth?
        3. **Coherence (1-5)**: Is the answer logical and well-structured?
        4. **Tool Selection (1/0)**: Did the agent use the right tools? (e.g. RAG for internal, Web for external)
        5. **Hallucination Check (0/1)**: 1 if NO hallucination, 0 if fabricated info.
        
        ### Output Format (JSON only)
        {{
            "goal_achievement": int,
            "accuracy_score": int,
            "coherence_score": int,
            "tool_selection_score": int,
            "no_hallucination_score": int,
            "reasoning": "string explanation" (Use language Vietnamese)
        }}
        """
        
        try:
            response = self.judge_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "You are a strict evaluator."},
                          {"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Evaluation failed: {e}")
            return {
                "goal_achievement": 0, "accuracy_score": 0, "coherence_score": 0, 
                "tool_selection_score": 0, "no_hallucination_score": 0, "reasoning": "Eval Error"
            }

    def calculate_cost(self, prompt_tokens: int, completion_tokens: int, model: str = "gpt-4o") -> float:
        """Calculate cost in VND based on OpenAI pricing (approximate)."""
        # Pricing per 1M tokens (USD)
        PRICING = {
            "gpt-4o": {"input": 5.0, "output": 15.0},
            "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
            "embedding": {"input": 0.02, "output": 0.0} # text-embedding-3-small
        }
        
        # Exchange rate
        USD_TO_VND = 25000
        
        if model not in PRICING:
            model = "gpt-4o" # Default to 4o pricing
            
        input_cost = (prompt_tokens / 1_000_000) * PRICING[model]["input"]
        output_cost = (completion_tokens / 1_000_000) * PRICING[model]["output"]
        
        total_usd = input_cost + output_cost
        return total_usd * USD_TO_VND

    def run(self):
        # 1. Setup
        self.setup_data()
        
        # 2. Load Dataset
        with open(DATASET_PATH, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
            
        results = []
        
        print(f"Starting Benchmark on {len(dataset)} test cases...")
        
        # 3. Execution Loop
        for case in tqdm(dataset):
            logger = {}
            logger['id'] = case['id']
            logger['category'] = case['category']
            logger['difficulty'] = case.get('difficulty', 'Unknown')
            logger['question'] = case['question']
            
            # --- Measure Efficiency ---
            start_time = time.time()
            total_tokens_input = 0
            total_tokens_output = 0
            
            try:
                # Run Agent
                response_obj = self.agent.run(case['question'], thread_id=f"bench_{case['id']}")
                actual_answer = response_obj.get("answer", "")
                execution_details = response_obj.get("execution_details", [])
                plan = response_obj.get("plan", [])
                
                # Count steps
                steps_count = len(execution_details) + len(plan)
                
                # Estimate tokens (Note: Real token usage requires CallbackHandler or API response usage field)
                # Since LangGraph generic response might not propagate usage easily without setup, 
                # we will estimate based on string length (1 token ~= 4 chars) for this POC.
                # In production, use get_openai_callback() from langchain-community.
                
                # Approximate input: Query + System Prompts (est. 1000) + Tool Outputs
                # Approximate output: Final Answer + Thoughts
                
                est_input_chars = len(case['question']) + 2000 # Base context
                for step in execution_details:
                    est_input_chars += len(str(step.get('output', '')))
                
                est_output_chars = len(actual_answer) + len(str(plan))
                
                total_tokens_input = est_input_chars // 4
                total_tokens_output = est_output_chars // 4
                
            except Exception as e:
                actual_answer = f"ERROR: {str(e)}"
                execution_details = []
                steps_count = 0
                
            end_time = time.time()
            latency = end_time - start_time
            
            # --- Calculate Cost ---
            # Assuming GPT-4o for main agent
            cost_vnd = self.calculate_cost(total_tokens_input, total_tokens_output, "gpt-4o")
            
            # --- Evaluate Quality ---
            eval_metrics = self.evaluate_response(
                case['question'], 
                case['expected_answer'], 
                actual_answer, 
                execution_details
            )
            
            # --- Aggregate Data ---
            logger.update({
                "latency_sec": round(latency, 2),
                "steps": steps_count,
                "tokens_input": total_tokens_input,
                "tokens_output": total_tokens_output,
                "est_cost_vnd": round(cost_vnd, 2),
                "actual_answer": actual_answer,
                **eval_metrics
            })
            
            results.append(logger)
            
        # 4. Reporting
        df = pd.DataFrame(results)
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig') # utf-8-sig for Excel compatibility
        
        print("\n" + "="*60)
        print("BENCHMARK SUMMARY")
        print("="*60)
        print(f"Total Cases: {len(df)}")
        print(f"Goal Achievement Rate: {df['goal_achievement'].mean()*100:.1f}%")
        print(f"Avg Accuracy (1-5): {df['accuracy_score'].mean():.2f}")
        print(f"Avg Latency: {df['latency_sec'].mean():.2f}s")
        print(f"Avg Cost per Query: {df['est_cost_vnd'].mean():.2f} VND")
        print(f"Total Cost: {df['est_cost_vnd'].sum():.2f} VND")
        print(f"Tool Selection Rate: {df['tool_selection_score'].mean()*100:.1f}%")
        
        print("\n" + "-"*60)
        print("BREAKDOWN BY DIFFICULTY")
        print("-"*60)
        if 'difficulty' in df.columns:
            # Group by difficulty and calculate means for numeric columns
            numeric_cols = ['goal_achievement', 'accuracy_score', 'latency_sec', 'est_cost_vnd', 'tool_selection_score']
            # Ensure columns exist before grouping (handling empty df or missing cols)
            available_cols = [c for c in numeric_cols if c in df.columns]
            
            if available_cols:
                difficulty_grp = df.groupby('difficulty')[available_cols].mean()
                
                # Add count column
                difficulty_grp['count'] = df['difficulty'].value_counts()
                
                # Format for display (percentage for rate columns)
                display_df = difficulty_grp.copy()
                if 'goal_achievement' in display_df:
                    display_df['goal_achievement'] = (display_df['goal_achievement'] * 100).apply(lambda x: f"{x:.1f}%")
                if 'tool_selection_score' in display_df:
                    display_df['tool_selection_score'] = (display_df['tool_selection_score'] * 100).apply(lambda x: f"{x:.1f}%")
                if 'est_cost_vnd' in display_df:
                    display_df['est_cost_vnd'] = display_df['est_cost_vnd'].apply(lambda x: f"{x:.2f}")
                if 'accuracy_score' in display_df:
                    display_df['accuracy_score'] = display_df['accuracy_score'].apply(lambda x: f"{x:.2f}")
                if 'latency_sec' in display_df:
                    display_df['latency_sec'] = display_df['latency_sec'].apply(lambda x: f"{x:.2f}s")

                print(tabulate(display_df, headers='keys', tablefmt='grid'))
                
        print("="*60)
        print(f"Detailed results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    bench = Benchmarker()
    bench.run()
