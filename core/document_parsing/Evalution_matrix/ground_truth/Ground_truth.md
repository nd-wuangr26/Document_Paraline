# Optimized Table Tokenization for Table Structure
Recognition
Maksym Lysak[0000−0002−3723−6960], Ahmed Nassar[0000−0002−9468−0822],
Nikolaos Livathinos[0000−0001−8513−3491], Christoph Auer[0000−0001−5761−0422],
and Peter Staar[0000−0002−8088−0823]
IBM Research
{mly,ahn,nli,cau,taa}@zurich.ibm.com
Abstract. Extracting tables from documents is a crucial task in any
document conversion pipeline. Recently, transformer-based models have
demonstrated that table-structure can be recognized with impressive ac-
curacy using Image-to-Markup-Sequence (Im2Seq) approaches. Taking
only the image of a table, such models predict a sequence of tokens (e.g.
in HTML, LaTeX) which represent the structure of the table. Since the
token representation of the table structure has a signiﬁcant impact on
the accuracy and run-time performance of any Im2Seq model, we inves-
tigate in this paper how table-structure representation can be optimised.
We propose a new, optimised table-structure language (OTSL) with a
minimized vocabulary and speciﬁc rules. The beneﬁts of OTSL are that
it reduces the number of tokens to 5 (HTML needs 28+) and shortens
the sequence length to half of HTML on average. Consequently, model
accuracy improves signiﬁcantly, inference time is halved compared to
HTML-based models, and the predicted table structures are always syn-
tactically correct. This in turn eliminates most post-processing needs.
Popular table structure data-sets will be published in OTSL format to
the community.
Keywords: Table Structure Recognition · Data Representation · Trans-
formers · Optimization.
## 1 Introduction
Tables are ubiquitous in documents such as scientiﬁc papers, patents, reports,
manuals, speciﬁcation sheets or marketing material. They often encode highly
valuable information and therefore need to be extracted with high accuracy.
Unfortunately, tables appear in documents in various sizes, styling and struc-
ture, making it diﬃcult to recover their correct structure with simple analyt-
ical methods. Therefore, accurate table extraction is achieved these days with
machine-learning based methods.
In modern document understanding systems [1,15], table extraction is typi-
cally a two-step process. Firstly, every table on a page is located with a bounding
box, and secondly, their logical row and column structure is recognized. As of
arXiv:2305.03393v1  [cs.CV]  5 May 2023

Optimized Table Tokenization for Table Structure Recognition
3
While the majority of research in TSR is currently focused on the develop-
ment and application of novel neural model architectures, the table structure
representation language (e.g. HTML in PubTabNet and FinTabNet) is usually
adopted as is for the sequence tokenization in Im2Seq models. In this paper,
we aim for the opposite and investigate the impact of the table structure rep-
resentation language with an otherwise unmodiﬁed Im2Seq transformer-based
architecture. Since the current state-of-the-art Im2Seq model is TableFormer [9],
we select this model to perform our experiments.
The main contribution of this paper is the introduction of a new optimised ta-
ble structure language (OTSL), speciﬁcally designed to describe table-structure
in an compact and structured way for Im2Seq models. OTSL has a number of
key features, which make it very attractive to use in Im2Seq models. Speciﬁcally,
compared to other languages such as HTML, OTSL has a minimized vocabulary
which yields short sequence length, strong inherent structure (e.g. strict rectan-
gular layout) and a strict syntax with rules that only look backwards. The latter
allows for syntax validation during inference and ensures a syntactically correct
table-structure. These OTSL features are illustrated in Figure 1, in comparison
to HTML.
The paper is structured as follows. In section 2, we give an overview of the
latest developments in table-structure reconstruction. In section 3 we review
the current HTML table encoding (popularised by PubTabNet and FinTabNet)
and discuss its ﬂaws. Subsequently, we introduce OTSL in section 4, which in-
cludes the language deﬁnition, syntax rules and error-correction procedures. In
section 5, we apply OTSL on the TableFormer architecture, compare it to Table-
Former models trained on HTML and ultimately demonstrate the advantages
of using OTSL. Finally, in section 6 we conclude our work and outline next
potential steps.
## 2 Related Work
Approaches to formalize the logical structure and layout of tables in electronic
documents date back more than two decades [16]. In the recent past, a wide
variety of computer vision methods have been explored to tackle the prob-
lem of table structure recognition, i.e. the correct identiﬁcation of columns,
rows and spanning cells in a given table. Broadly speaking, the current deep-
learning based approaches fall into three categories: object detection (OD) meth-
ods, Graph-Neural-Network (GNN) methods and Image-to-Markup-Sequence
(Im2Seq) methods. Object-detection based methods [11,12,13,14,21] rely on table-
structure annotation using (overlapping) bounding boxes for training, and pro-
duce bounding-box predictions to deﬁne table cells, rows, and columns on a table
image. Graph Neural Network (GNN) based methods [3,6,17,18], as the name
suggests, represent tables as graph structures. The graph nodes represent the
content of each table cell, an embedding vector from the table image, or geomet-
ric coordinates of the table cell. The edges of the graph deﬁne the relationship
between the nodes, e.g. if they belong to the same column, row, or table cell.

4
M. Lysak, et al.
Other work [20] aims at predicting a grid for each table and deciding which cells
must be merged using an attention network. Im2Seq methods cast the problem
as a sequence generation task [4,5,9,22], and therefore need an internal table-
structure representation language, which is often implemented with standard
markup languages (e.g. HTML, LaTeX, Markdown). In theory, Im2Seq methods
have a natural advantage over the OD and GNN methods by virtue of directly
predicting the table-structure. As such, no post-processing or rules are needed
in order to obtain the table-structure, which is necessary with OD and GNN
approaches. In practice, this is not entirely true, because a predicted sequence
of table-structure markup does not necessarily have to be syntactically correct.
Hence, depending on the quality of the predicted sequence, some post-processing
needs to be performed to ensure a syntactically valid (let alone correct) sequence.
Within the Im2Seq method, we ﬁnd several popular models, namely the
encoder-dual-decoder model (EDD) [22], TableFormer [9], Tabsplitter[2] and Ye
et. al. [19]. EDD uses two consecutive long short-term memory (LSTM) decoders
to predict a table in HTML representation. The tag decoder predicts a sequence
of HTML tags. For each decoded table cell (<td>), the attention is passed to
the cell decoder to predict the content with an embedded OCR approach. The
latter makes it susceptible to transcription errors in the cell content of the table.
TableFormer address this reliance on OCR and uses two transformer decoders for
HTML structure and cell bounding box prediction in an end-to-end architecture.
The predicted cell bounding box is then used to extract text tokens from an
originating (digital) PDF page, circumventing any need for OCR. TabSplitter
[2] proposes a compact double-matrix representation of table rows and columns
to do error detection and error correction of HTML structure sequences based
on predictions from [19]. This compact double-matrix representation can not be
used directly by the Img2seq model training, so the model uses HTML as an
intermediate form. Chi et. al. [4] introduce a data set and a baseline method
using bidirectional LSTMs to predict LaTeX code. Kayal [5] introduces Gated
ResNet transformers to predict LaTeX code, and a separate OCR module to
extract content.
Im2Seq approaches have shown to be well-suited for the TSR task and allow a
full end-to-end network design that can output the ﬁnal table structure without
pre- or post-processing logic. Furthermore, Im2Seq models have demonstrated
to deliver state-of-the-art prediction accuracy [9]. This motivated the authors
to investigate if the performance (both in accuracy and inference time) can
be further improved by optimising the table structure representation language.
We believe this is a necessary step before further improving neural network
architectures for this task.
## 3 Problem Statement
All known Im2Seq based models for TSR fundamentally work in similar ways.
Given an image of a table, the Im2Seq model predicts the structure of the table
by generating a sequence of tokens. These tokens originate from a ﬁnite vocab-

6
M. Lysak, et al.
generation. Implicitly, this also means that Im2Seq models need to learn these
complex syntax rules, simply to deliver valid output.
In practice, we observe two major issues with prediction quality when train-
ing Im2Seq models on HTML table structure generation from images. On the
one hand, we ﬁnd that on large tables, the visual attention of the model often
starts to drift and is not accurately moving forward cell by cell anymore. This
manifests itself in either in an increasing location drift for proposed table-cells
in later rows on the same column or even complete loss of vertical alignment, as
illustrated in Figure 5. Addressing this with post-processing is partially possible,
but clearly undesired. On the other hand, we ﬁnd many instances of predictions
with structural inconsistencies or plain invalid HTML output, as shown in Fig-
ure 6, which are nearly impossible to properly correct. Both problems seriously
impact the TSR model performance, since they reﬂect not only in the task of
pure structure recognition but also in the equally crucial recognition or matching
of table cell content.
## 4 Optimised Table Structure Language
To mitigate the issues with HTML in Im2Seq-based TSR models laid out before,
we propose here our Optimised Table Structure Language (OTSL). OTSL is
designed to express table structure with a minimized vocabulary and a simple
set of rules, which are both signiﬁcantly reduced compared to HTML. At the
same time, OTSL enables easy error detection and correction during sequence
generation. We further demonstrate how the compact structure representation
and minimized sequence length improves prediction accuracy and inference time
in the TableFormer architecture.
### 4.1 Language Deﬁnition
In Figure 3, we illustrate how the OTSL is deﬁned. In essence, the OTSL deﬁnes
only 5 tokens that directly describe a tabular structure based on an atomic 2D
grid.
The OTSL vocabulary is comprised of the following tokens:
– "C" cell - a new table cell that either has or does not have cell content
– "L" cell - left-looking cell, merging with the left neighbor cell to create a
span
– "U" cell - up-looking cell, merging with the upper neighbor cell to create a
span
– "X" cell - cross cell, to merge with both left and upper neighbor cells
– "NL" - new-line, switch to the next row.
A notable attribute of OTSL is that it has the capability of achieving lossless
conversion to HTML.

12
M. Lysak, et al.
## 6 Conclusion
We demonstrated that representing tables in HTML for the task of table struc-
ture recognition with Im2Seq models is ill-suited and has serious limitations.
Furthermore, we presented in this paper an Optimized Table Structure Language
(OTSL) which, when compared to commonly used general purpose languages,
has several key beneﬁts.
First and foremost, given the same network conﬁguration, inference time for
a table-structure prediction is about 2 times faster compared to the conventional
HTML approach. This is primarily owed to the shorter sequence length of the
OTSL representation. Additional performance beneﬁts can be obtained with
HPO (hyper parameter optimization). As we demonstrate in our experiments,
models trained on OTSL can be signiﬁcantly smaller, e.g. by reducing the number
of encoder and decoder layers, while preserving comparatively good prediction
quality. This can further improve inference performance, yielding 5-6 times faster
inference speed in OTSL with prediction quality comparable to models trained
on HTML (see Table 1).
Secondly, OTSL has more inherent structure and a signiﬁcantly restricted vo-
cabulary size. This allows autoregressive models to perform better in the TED
metric, but especially with regards to prediction accuracy of the table-cell bound-
ing boxes (see Table 2). As shown in Figure 5, we observe that the OTSL dras-
tically reduces the drift for table cell bounding boxes at high row count and in
sparse tables. This leads to more accurate predictions and a signiﬁcant reduction
in post-processing complexity, which is an undesired necessity in HTML-based
Im2Seq models. Signiﬁcant novelty lies in OTSL syntactical rules, which are few,
simple and always backwards looking. Each new token can be validated only by
analyzing the sequence of previous tokens, without requiring the entire sequence
to detect mistakes. This in return allows to perform structural error detection
and correction on-the-ﬂy during sequence generation.
## References

1. Auer, C., Dolﬁ, M., Carvalho, A., Ramis, C.B., Staar, P.W.J.: Delivering doc-
ument conversion as a cloud service with high throughput and responsiveness.
CoRR abs/2206.00785 (2022). https://doi.org/10.48550/arXiv.2206.00785,
https://doi.org/10.48550/arXiv.2206.00785
2. Chen, B., Peng, D., Zhang, J., Ren, Y., Jin, L.: Complex table structure recognition
in the wild using transformer and identity matrix-based augmentation. In: Porwal,
U., Fornés, A., Shafait, F. (eds.) Frontiers in Handwriting Recognition. pp. 545–
561. Springer International Publishing, Cham (2022)
3. Chi, Z., Huang, H., Xu, H.D., Yu, H., Yin, W., Mao, X.L.: Complicated table
structure recognition. arXiv preprint arXiv:1908.04729 (2019)
4. Deng, Y., Rosenberg, D., Mann, G.: Challenges in end-to-end neural scientiﬁc
table recognition. In: 2019 International Conference on Document Analysis and
Recognition (ICDAR). pp. 894–901. IEEE (2019)
Optimized Table Tokenization for Table Structure Recognition 13
5. Kayal, P., Anand, M., Desai, H., Singh, M.: Tables to latex: structure and content
extraction from scientiﬁc tables. International Journal on Document Analysis and
Recognition (IJDAR) pp. 1–10 (2022)
6. Lee, E., Kwon, J., Yang, H., Park, J., Lee, S., Koo, H.I., Cho, N.I.: Table structure
recognition based on grid shape graph. In: 2022 Asia-Paciﬁc Signal and Information
Processing Association Annual Summit and Conference (APSIPA ASC). pp. 1868 – 1873. IEEE (2022)
7. Li, M., Cui, L., Huang, S., Wei, F., Zhou, M., Li, Z.: Tablebank: A benchmark
dataset for table detection and recognition (2019)
8. Livathinos, N., Berrospi, C., Lysak, M., Kuropiatnyk, V., Nassar, A., Carvalho,
A., Dolﬁ, M., Auer, C., Dinkla, K., Staar, P.: Robust pdf document conversion
using recurrent neural networks. Proceedings of the AAAI Conference on Artiﬁcial
Intelligence 35(17), 15137–15145 (May 2021), https://ojs.aaai.org/index.php/
AAAI/article/view/17777
9. Nassar, A., Livathinos, N., Lysak, M., Staar, P.: Tableformer: Table structure un-
derstanding with transformers. In: Proceedings of the IEEE/CVF Conference on
Computer Vision and Pattern Recognition (CVPR). pp. 4614–4623 (June 2022)
10. Pﬁtzmann, B., Auer, C., Dolﬁ, M., Nassar, A.S., Staar, P.W.J.: Doclaynet: A
large human-annotated dataset for document-layout segmentation. In: Zhang, A.,
Rangwala, H. (eds.) KDD ’22: The 28th ACM SIGKDD Conference on Knowledge
Discovery and Data Mining, Washington, DC, USA, August 14 - 18, 2022. pp.
3743–3751. ACM (2022). https://doi.org/10.1145/3534678.3539043, https://
doi.org/10.1145/3534678.3539043
11. Prasad, D., Gadpal, A., Kapadni, K., Visave, M., Sultanpure, K.: Cascadetabnet:
An approach for end to end table detection and structure recognition from image-
based documents. In: Proceedings of the IEEE/CVF conference on computer vision
and pattern recognition workshops. pp. 572–573 (2020)
12. Schreiber, S., Agne, S., Wolf, I., Dengel, A., Ahmed, S.: Deepdesrt: Deep learning
for detection and structure recognition of tables in document images. In: 2017 14th
IAPR international conference on document analysis and recognition (ICDAR).
vol. 1, pp. 1162–1167. IEEE (2017)
13. Siddiqui, S.A., Fateh, I.A., Rizvi, S.T.R., Dengel, A., Ahmed, S.: Deeptabstr: Deep
learning based table structure recognition. In: 2019 International Conference on
Document Analysis and Recognition (ICDAR). pp. 1403–1409 (2019). https://
doi.org/10.1109/ICDAR.2019.00226
14. Smock, B., Pesala, R., Abraham, R.: PubTables-1M: Towards comprehensive ta-
ble extraction from unstructured documents. In: Proceedings of the IEEE/CVF
Conference on Computer Vision and Pattern Recognition (CVPR). pp. 4634–4642
(June 2022)
15. Staar, P.W.J., Dolﬁ, M., Auer, C., Bekas, C.: Corpus conversion service: A ma-
chine learning platform to ingest documents at scale. In: Proceedings of the 24th
ACM SIGKDD International Conference on Knowledge Discovery & Data Min-
ing. pp. 774–782. KDD ’18, Association for Computing Machinery, New York, NY,
USA (2018). https://doi.org/10.1145/3219819.3219834, https://doi.org/10.
1145/3219819.3219834
16. Wang, X.: Tabular Abstraction, Editing, and Formatting. Ph.D. thesis, CAN
(1996), aAINN09397
17. Xue, W., Li, Q., Tao, D.: Res2tim: Reconstruct syntactic structures from table
images. In: 2019 International Conference on Document Analysis and Recognition
(ICDAR). pp. 749–755. IEEE (2019) 14
M. Lysak, et al.
18. Xue, W., Yu, B., Wang, W., Tao, D., Li, Q.: Tgrnet: A table graph reconstruc-
tion network for table structure recognition. In: Proceedings of the IEEE/CVF
International Conference on Computer Vision. pp. 1295–1304 (2021)
19. Ye, J., Qi, X., He, Y., Chen, Y., Gu, D., Gao, P., Xiao, R.: Pingan-vcgroup’s
solution for icdar 2021 competition on scientiﬁc literature parsing task b: Ta-
ble recognition to html (2021). https://doi.org/10.48550/ARXIV.2105.01848,
https://arxiv.org/abs/2105.01848
20. Zhang, Z., Zhang, J., Du, J., Wang, F.: Split, embed and merge: An accurate table
structure recognizer. Pattern Recognition 126, 108565 (2022)
21. Zheng, X., Burdick, D., Popa, L., Zhong, X., Wang, N.X.R.: Global table extractor
(gte): A framework for joint table identiﬁcation and cell structure recognition using
visual context. In: 2021 IEEE Winter Conference on Applications of Computer Vi-
sion (WACV). pp. 697–706 (2021). https://doi.org/10.1109/WACV48630.2021.
00074
22. Zhong, X., ShaﬁeiBavani, E., Jimeno Yepes, A.: Image-based table recognition:
Data, model, and evaluation. In: Vedaldi, A., Bischof, H., Brox, T., Frahm, J.M.
(eds.) Computer Vision – ECCV 2020. pp. 564–580. Springer International Pub-
lishing, Cham (2020)
23. Zhong, X., Tang, J., Yepes, A.J.: Publaynet: largest dataset ever for document lay-
out analysis. In: 2019 International Conference on Document Analysis and Recog-
nition (ICDAR). pp. 1015–1022. IEEE (2019)

