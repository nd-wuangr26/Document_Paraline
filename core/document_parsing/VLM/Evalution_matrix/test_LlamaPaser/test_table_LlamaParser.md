
## 5.1 Hyper Parameter Optimization

<table>
    <thead>
    <tr>
        <th rowspan="2">#

enc-layers</th>
        <th rowspan="2">#

dec-layers</th>
        <th rowspan="2">Language</th>
        <th colspan="3">TEDs</th>
        <th rowspan="2">mAP

(0.75)</th>
        <th rowspan="2">Inference

time (secs)</th>
    </tr>
    <tr>
        <th>simple</th>
        <th>complex</th>
        <th>all</th>
    </tr>
    </thead>
    <tr>
        <td>6</td>
        <td>6</td>
        <td>OTSL

HTML</td>
        <td>0.965

0.969</td>
        <td>0.934

0.927</td>
        <td>0.955

0.955</td>
        <td>0.88

0.857</td>
        <td>2.73

5.39</td>
    </tr>
    <tr>
        <td>4</td>
        <td>4</td>
        <td>OTSL

HTML</td>
        <td>0.938

0.952</td>
        <td>0.904

0.909</td>
        <td>0.927

0.938</td>
        <td>0.853

0.843</td>
        <td>1.97

3.77</td>
    </tr>
    <tr>
        <td>2</td>
        <td>4</td>
        <td>OTSL

HTML</td>
        <td>0.923

0.945</td>
        <td>0.897

0.901</td>
        <td>0.915

0.931</td>
        <td>0.859

0.834</td>
        <td>1.91

3.81</td>
    </tr>
    <tr>
        <td>4</td>
        <td>2</td>
        <td>OTSL

HTML</td>
        <td>0.952

0.944</td>
        <td>0.92

0.903</td>
        <td>0.942

0.931</td>
        <td>0.857

0.824</td>
        <td>1.22

2</td>
    </tr></table>

## 5.2 Quantitative Results

<table>
  <thead>
    <tr>
      <th>Data set</th>
      <th>Language</th>
      <th colspan="3">TEDs</th>
      <th>mAP(0.75)</th>
      <th>Inference time (secs)</th>
    </tr>
<tr>
      <th></th>
      <th></th>
      <th>simple</th>
      <th>complex</th>
      <th>all</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="2">PubTabNet</td>
      <td>OTSL</td>
      <td>0.965</td>
      <td>0.934</td>
      <td>0.955</td>
      <td><b>0.88</b></td>
      <td><b>2.73</b></td>
    </tr>
<tr>
      <td>HTML</td>
      <td>0.969</td>
      <td>0.927</td>
      <td>0.955</td>
      <td>0.857</td>
      <td>5.39</td>
    </tr>
<tr>
      <td rowspan="2">FinTabNet</td>
      <td>OTSL</td>
      <td>0.955</td>
      <td>0.961</td>
      <td><b>0.959</b></td>
      <td><b>0.862</b></td>
      <td><b>1.85</b></td>
    </tr>
<tr>
      <td>HTML</td>
      <td>0.917</td>
      <td>0.922</td>
      <td>0.92</td>
      <td>0.722</td>
      <td>3.26</td>
    </tr>
<tr>
      <td rowspan="2">PubTables-1M</td>
      <td>OTSL</td>
      <td>0.987</td>
      <td>0.964</td>
      <td><b>0.977</b></td>
      <td><b>0.896</b></td>
      <td><b>1.79</b></td>
    </tr>
<tr>
      <td>HTML</td>
      <td>0.983</td>
      <td>0.944</td>
      <td>0.966</td>
      <td>0.889</td>
      <td>3.26</td>
    </tr>
  </tbody>
</table>