# Statistical Evaluation of Techniques
## MCC
|       U | algorithm 1   | algorithm 2   |   cliff_delta |   mean algorithm 1 |   mean algorithm 2 | measure   |     p-value |   p-value corrected | significant   |
|--------:|:--------------|:--------------|--------------:|-------------------:|-------------------:|:----------|------------:|--------------------:|:--------------|
|  2815.5 | agglomerative | birch         |       -0.4369 |             0.5071 |             0.5641 | mcc       | 1           |         6           | no            |
|     0   | agglomerative | iqr           |       -1      |             0.5071 |             0.7952 | mcc       | 1           |         6           | no            |
|  1910   | agglomerative | kmeans        |       -0.618  |             0.5071 |             0.595  | mcc       | 1           |         6           | no            |
|  1483.5 | agglomerative | mahalanobis   |       -0.7033 |             0.5071 |             0.6034 | mcc       | 1           |         6           | no            |
|   971   | agglomerative | mean_shift    |       -0.8058 |             0.5071 |             0.6292 | mcc       | 1           |         6           | no            |
|  7184.5 | birch         | agglomerative |        0.4369 |             0.5641 |             0.5071 | mcc       | 4.73634e-08 |         2.8418e-07  | **yes**       |
|     0   | birch         | iqr           |       -1      |             0.5641 |             0.7952 | mcc       | 1           |         6           | no            |
|  3552.5 | birch         | kmeans        |       -0.2895 |             0.5641 |             0.595  | mcc       | 0.999799    |         5.99879     | no            |
|  3492   | birch         | mahalanobis   |       -0.3016 |             0.5641 |             0.6034 | mcc       | 0.999886    |         5.99932     | no            |
|  2095.5 | birch         | mean_shift    |       -0.5809 |             0.5641 |             0.6292 | mcc       | 1           |         6           | no            |
| 10000   | iqr           | agglomerative |        1      |             0.7952 |             0.5071 | mcc       | 1.27151e-34 |         7.62905e-34 | **yes**       |
| 10000   | iqr           | birch         |        1      |             0.7952 |             0.5641 | mcc       | 1.27208e-34 |         7.63249e-34 | **yes**       |
| 10000   | iqr           | kmeans        |        1      |             0.7952 |             0.595  | mcc       | 1.27402e-34 |         7.64411e-34 | **yes**       |
| 10000   | iqr           | mahalanobis   |        1      |             0.7952 |             0.6034 | mcc       | 1.26843e-34 |         7.61059e-34 | **yes**       |
|  9996   | iqr           | mean_shift    |        0.9992 |             0.7952 |             0.6292 | mcc       | 1.43464e-34 |         8.60782e-34 | **yes**       |
|  8090   | kmeans        | agglomerative |        0.618  |             0.595  |             0.5071 | mcc       | 2.19259e-14 |         1.31555e-13 | **yes**       |
|  6447.5 | kmeans        | birch         |        0.2895 |             0.595  |             0.5641 | mcc       | 0.000203366 |         0.0012202   | **yes**       |
|     0   | kmeans        | iqr           |       -1      |             0.595  |             0.7952 | mcc       | 1           |         6           | no            |
|  5821.5 | kmeans        | mahalanobis   |        0.1643 |             0.595  |             0.6034 | mcc       | 0.0224222   |         0.134533    | no            |
|  3026.5 | kmeans        | mean_shift    |       -0.3947 |             0.595  |             0.6292 | mcc       | 0.999999    |         6           | no            |
|  8516.5 | mahalanobis   | agglomerative |        0.7033 |             0.6034 |             0.5071 | mcc       | 4.27884e-18 |         2.56731e-17 | **yes**       |
|  6508   | mahalanobis   | birch         |        0.3016 |             0.6034 |             0.5641 | mcc       | 0.000114985 |         0.000689909 | **yes**       |
|     0   | mahalanobis   | iqr           |       -1      |             0.6034 |             0.7952 | mcc       | 1           |         6           | no            |
|  4178.5 | mahalanobis   | kmeans        |       -0.1643 |             0.6034 |             0.595  | mcc       | 0.977708    |         5.86625     | no            |
|  2160   | mahalanobis   | mean_shift    |       -0.568  |             0.6034 |             0.6292 | mcc       | 1           |         6           | no            |
|  9029   | mean_shift    | agglomerative |        0.8058 |             0.6292 |             0.5071 | mcc       | 3.65574e-23 |         2.19344e-22 | **yes**       |
|  7904.5 | mean_shift    | birch         |        0.5809 |             0.6292 |             0.5641 | mcc       | 6.428e-13   |         3.8568e-12  | **yes**       |
|     4   | mean_shift    | iqr           |       -0.9992 |             0.6292 |             0.7952 | mcc       | 1           |         6           | no            |
|  6973.5 | mean_shift    | kmeans        |        0.3947 |             0.6292 |             0.595  | mcc       | 7.14501e-07 |         4.287e-06   | **yes**       |
|  7840   | mean_shift    | mahalanobis   |        0.568  |             0.6292 |             0.6034 | mcc       | 1.98362e-12 |         1.19017e-11 | **yes**       |
## F1
|       U | algorithm 1   | algorithm 2   |   cliff_delta |   mean algorithm 1 |   mean algorithm 2 | measure   |     p-value |   p-value corrected | significant   |
|--------:|:--------------|:--------------|--------------:|-------------------:|-------------------:|:----------|------------:|--------------------:|:--------------|
|  2158   | agglomerative | birch         |       -0.5684 |             0.4946 |             0.5909 | f1        | 1           |         6           | no            |
|     0   | agglomerative | iqr           |       -1      |             0.4946 |             0.8058 | f1        | 1           |         6           | no            |
|  1251.5 | agglomerative | kmeans        |       -0.7497 |             0.4946 |             0.6359 | f1        | 1           |         6           | no            |
|  1339   | agglomerative | mahalanobis   |       -0.7322 |             0.4946 |             0.6285 | f1        | 1           |         6           | no            |
|   970   | agglomerative | mean_shift    |       -0.806  |             0.4946 |             0.6494 | f1        | 1           |         6           | no            |
|  7842   | birch         | agglomerative |        0.5684 |             0.5909 |             0.4946 | f1        | 1.79027e-12 |         1.07416e-11 | **yes**       |
|     0   | birch         | iqr           |       -1      |             0.5909 |             0.8058 | f1        | 1           |         6           | no            |
|  3693.5 | birch         | kmeans        |       -0.2613 |             0.5909 |             0.6359 | f1        | 0.999329    |         5.99597     | no            |
|  5456.5 | birch         | mahalanobis   |        0.0913 |             0.5909 |             0.6285 | f1        | 0.132106    |         0.792633    | no            |
|  3051.5 | birch         | mean_shift    |       -0.3897 |             0.5909 |             0.6494 | f1        | 0.999999    |         5.99999     | no            |
| 10000   | iqr           | agglomerative |        1      |             0.8058 |             0.4946 | f1        | 1.12058e-34 |         6.72346e-34 | **yes**       |
| 10000   | iqr           | birch         |        1      |             0.8058 |             0.5909 | f1        | 1.11647e-34 |         6.6988e-34  | **yes**       |
| 10000   | iqr           | kmeans        |        1      |             0.8058 |             0.6359 | f1        | 1.05457e-34 |         6.32745e-34 | **yes**       |
| 10000   | iqr           | mahalanobis   |        1      |             0.8058 |             0.6285 | f1        | 1.07683e-34 |         6.461e-34   | **yes**       |
| 10000   | iqr           | mean_shift    |        1      |             0.8058 |             0.6494 | f1        | 1.06773e-34 |         6.40638e-34 | **yes**       |
|  8748.5 | kmeans        | agglomerative |        0.7497 |             0.6359 |             0.4946 | f1        | 2.21009e-20 |         1.32605e-19 | **yes**       |
|  6306.5 | kmeans        | birch         |        0.2613 |             0.6359 |             0.5909 | f1        | 0.000676822 |         0.00406093  | **yes**       |
|     0   | kmeans        | iqr           |       -1      |             0.6359 |             0.8058 | f1        | 1           |         6           | no            |
|  7022   | kmeans        | mahalanobis   |        0.4044 |             0.6359 |             0.6285 | f1        | 3.63604e-07 |         2.18162e-06 | **yes**       |
|  4208.5 | kmeans        | mean_shift    |       -0.1583 |             0.6359 |             0.6494 | f1        | 0.974198    |         5.84519     | no            |
|  8661   | mahalanobis   | agglomerative |        0.7322 |             0.6285 |             0.4946 | f1        | 1.5593e-19  |         9.35579e-19 | **yes**       |
|  4543.5 | mahalanobis   | birch         |       -0.0913 |             0.6285 |             0.5909 | f1        | 0.868417    |         5.2105      | no            |
|     0   | mahalanobis   | iqr           |       -1      |             0.6285 |             0.8058 | f1        | 1           |         6           | no            |
|  2978   | mahalanobis   | kmeans        |       -0.4044 |             0.6285 |             0.6359 | f1        | 1           |         6           | no            |
|  2366   | mahalanobis   | mean_shift    |       -0.5268 |             0.6285 |             0.6494 | f1        | 1           |         6           | no            |
|  9030   | mean_shift    | agglomerative |        0.806  |             0.6494 |             0.4946 | f1        | 2.939e-23   |         1.7634e-22  | **yes**       |
|  6948.5 | mean_shift    | birch         |        0.3897 |             0.6494 |             0.5909 | f1        | 8.84511e-07 |         5.30707e-06 | **yes**       |
|     0   | mean_shift    | iqr           |       -1      |             0.6494 |             0.8058 | f1        | 1           |         6           | no            |
|  5791.5 | mean_shift    | kmeans        |        0.1583 |             0.6494 |             0.6359 | f1        | 0.0259498   |         0.155699    | no            |
|  7634   | mean_shift    | mahalanobis   |        0.5268 |             0.6494 |             0.6285 | f1        | 5.47944e-11 |         3.28766e-10 | **yes**       |
## PRECISION
|      U | algorithm 1   | algorithm 2   |   cliff_delta |   mean algorithm 1 |   mean algorithm 2 | measure   |     p-value |   p-value corrected | significant   |
|-------:|:--------------|:--------------|--------------:|-------------------:|-------------------:|:----------|------------:|--------------------:|:--------------|
| 8778.5 | agglomerative | birch         |        0.7557 |             0.816  |             0.6444 | precision | 1.09987e-20 |         6.59921e-20 | **yes**       |
| 9155.5 | agglomerative | iqr           |        0.8311 |             0.816  |             0.682  | precision | 1.17605e-24 |         7.05628e-24 | **yes**       |
| 9908.5 | agglomerative | kmeans        |        0.9817 |             0.816  |             0.5943 | precision | 1.42816e-33 |         8.56897e-33 | **yes**       |
| 6831.5 | agglomerative | mahalanobis   |        0.3663 |             0.816  |             0.7655 | precision | 3.26957e-06 |         1.96174e-05 | **yes**       |
| 8256   | agglomerative | mean_shift    |        0.6512 |             0.816  |             0.6331 | precision | 7.66378e-16 |         4.59827e-15 | **yes**       |
| 1221.5 | birch         | agglomerative |       -0.7557 |             0.6444 |             0.816  | precision | 1           |         6           | no            |
| 2958.5 | birch         | iqr           |       -0.4083 |             0.6444 |             0.682  | precision | 1           |         6           | no            |
| 5450.5 | birch         | kmeans        |        0.0901 |             0.6444 |             0.5943 | precision | 0.135645    |         0.81387     | no            |
| 1612   | birch         | mahalanobis   |       -0.6776 |             0.6444 |             0.7655 | precision | 1           |         6           | no            |
| 5782.5 | birch         | mean_shift    |        0.1565 |             0.6444 |             0.6331 | precision | 0.0279209   |         0.167525    | no            |
|  844.5 | iqr           | agglomerative |       -0.8311 |             0.682  |             0.816  | precision | 1           |         6           | no            |
| 7041.5 | iqr           | birch         |        0.4083 |             0.682  |             0.6444 | precision | 3.02183e-07 |         1.8131e-06  | **yes**       |
| 7962   | iqr           | kmeans        |        0.5924 |             0.682  |             0.5943 | precision | 2.21897e-13 |         1.33138e-12 | **yes**       |
| 1708   | iqr           | mahalanobis   |       -0.6584 |             0.682  |             0.7655 | precision | 1           |         6           | no            |
| 7097.5 | iqr           | mean_shift    |        0.4195 |             0.682  |             0.6331 | precision | 1.47179e-07 |         8.83077e-07 | **yes**       |
|   91.5 | kmeans        | agglomerative |       -0.9817 |             0.5943 |             0.816  | precision | 1           |         6           | no            |
| 4549.5 | kmeans        | birch         |       -0.0901 |             0.5943 |             0.6444 | precision | 0.864887    |         5.18932     | no            |
| 2038   | kmeans        | iqr           |       -0.5924 |             0.5943 |             0.682  | precision | 1           |         6           | no            |
|  345   | kmeans        | mahalanobis   |       -0.931  |             0.5943 |             0.7655 | precision | 1           |         6           | no            |
| 5219   | kmeans        | mean_shift    |        0.0438 |             0.5943 |             0.6331 | precision | 0.296632    |         1.77979     | no            |
| 3168.5 | mahalanobis   | agglomerative |       -0.3663 |             0.7655 |             0.816  | precision | 0.999997    |         5.99998     | no            |
| 8388   | mahalanobis   | birch         |        0.6776 |             0.7655 |             0.6444 | precision | 5.74085e-17 |         3.44451e-16 | **yes**       |
| 8292   | mahalanobis   | iqr           |        0.6584 |             0.7655 |             0.682  | precision | 3.72467e-16 |         2.2348e-15  | **yes**       |
| 9655   | mahalanobis   | kmeans        |        0.931  |             0.7655 |             0.5943 | precision | 2.38736e-30 |         1.43241e-29 | **yes**       |
| 7987.5 | mahalanobis   | mean_shift    |        0.5975 |             0.7655 |             0.6331 | precision | 1.35443e-13 |         8.12657e-13 | **yes**       |
| 1744   | mean_shift    | agglomerative |       -0.6512 |             0.6331 |             0.816  | precision | 1           |         6           | no            |
| 4217.5 | mean_shift    | birch         |       -0.1565 |             0.6331 |             0.6444 | precision | 0.972236    |         5.83341     | no            |
| 2902.5 | mean_shift    | iqr           |       -0.4195 |             0.6331 |             0.682  | precision | 1           |         6           | no            |
| 4781   | mean_shift    | kmeans        |       -0.0438 |             0.6331 |             0.5943 | precision | 0.704213    |         4.22528     | no            |
| 2012.5 | mean_shift    | mahalanobis   |       -0.5975 |             0.6331 |             0.7655 | precision | 1           |         6           | no            |
## RECALL
|       U | algorithm 1   | algorithm 2   |   cliff_delta |   mean algorithm 1 |   mean algorithm 2 | measure   |     p-value |   p-value corrected | significant   |
|--------:|:--------------|:--------------|--------------:|-------------------:|-------------------:|:----------|------------:|--------------------:|:--------------|
|  1464.5 | agglomerative | birch         |       -0.7071 |             0.3768 |             0.631  | recall    | 1           |         6           | no            |
|     0   | agglomerative | iqr           |       -1      |             0.3768 |             0.9896 | recall    | 1           |         6           | no            |
|   343.5 | agglomerative | kmeans        |       -0.9313 |             0.3768 |             0.7209 | recall    | 1           |         6           | no            |
|  1648   | agglomerative | mahalanobis   |       -0.6704 |             0.3768 |             0.5376 | recall    | 1           |         6           | no            |
|   666.5 | agglomerative | mean_shift    |       -0.8667 |             0.3768 |             0.7727 | recall    | 1           |         6           | no            |
|  8535.5 | birch         | agglomerative |        0.7071 |             0.631  |             0.3768 | recall    | 2.71443e-18 |         1.62866e-17 | **yes**       |
|     0   | birch         | iqr           |       -1      |             0.631  |             0.9896 | recall    | 1           |         6           | no            |
|  3890   | birch         | kmeans        |       -0.222  |             0.631  |             0.7209 | recall    | 0.99669     |         5.98014     | no            |
|  8214   | birch         | mahalanobis   |        0.6428 |             0.631  |             0.5376 | recall    | 1.85899e-15 |         1.11539e-14 | **yes**       |
|  3148   | birch         | mean_shift    |       -0.3704 |             0.631  |             0.7727 | recall    | 0.999997    |         5.99998     | no            |
| 10000   | iqr           | agglomerative |        1      |             0.9896 |             0.3768 | recall    | 1.23811e-36 |         7.42866e-36 | **yes**       |
| 10000   | iqr           | birch         |        1      |             0.9896 |             0.631  | recall    | 1.27083e-36 |         7.62497e-36 | **yes**       |
|  9905.5 | iqr           | kmeans        |        0.9811 |             0.9896 |             0.7209 | recall    | 2.12078e-35 |         1.27247e-34 | **yes**       |
| 10000   | iqr           | mahalanobis   |        1      |             0.9896 |             0.5376 | recall    | 1.06799e-36 |         6.40796e-36 | **yes**       |
|  7909   | iqr           | mean_shift    |        0.5818 |             0.9896 |             0.7727 | recall    | 2.92515e-15 |         1.75509e-14 | **yes**       |
|  9656.5 | kmeans        | agglomerative |        0.9313 |             0.7209 |             0.3768 | recall    | 2.53312e-30 |         1.51987e-29 | **yes**       |
|  6110   | kmeans        | birch         |        0.222  |             0.7209 |             0.631  | recall    | 0.00333489  |         0.0200093   | no            |
|    94.5 | kmeans        | iqr           |       -0.9811 |             0.7209 |             0.9896 | recall    | 1           |         6           | no            |
|  9138.5 | kmeans        | mahalanobis   |        0.8277 |             0.7209 |             0.5376 | recall    | 2.1158e-24  |         1.26948e-23 | **yes**       |
|  4025   | kmeans        | mean_shift    |       -0.195  |             0.7209 |             0.7727 | recall    | 0.991597    |         5.94958     | no            |
|  8352   | mahalanobis   | agglomerative |        0.6704 |             0.5376 |             0.3768 | recall    | 9.90193e-17 |         5.94116e-16 | **yes**       |
|  1786   | mahalanobis   | birch         |       -0.6428 |             0.5376 |             0.631  | recall    | 1           |         6           | no            |
|     0   | mahalanobis   | iqr           |       -1      |             0.5376 |             0.9896 | recall    | 1           |         6           | no            |
|   861.5 | mahalanobis   | kmeans        |       -0.8277 |             0.5376 |             0.7209 | recall    | 1           |         6           | no            |
|  1408.5 | mahalanobis   | mean_shift    |       -0.7183 |             0.5376 |             0.7727 | recall    | 1           |         6           | no            |
|  9333.5 | mean_shift    | agglomerative |        0.8667 |             0.7727 |             0.3768 | recall    | 1.19483e-26 |         7.169e-26   | **yes**       |
|  6852   | mean_shift    | birch         |        0.3704 |             0.7727 |             0.631  | recall    | 2.83102e-06 |         1.69861e-05 | **yes**       |
|  2091   | mean_shift    | iqr           |       -0.5818 |             0.7727 |             0.9896 | recall    | 1           |         6           | no            |
|  5975   | mean_shift    | kmeans        |        0.195  |             0.7727 |             0.7209 | recall    | 0.00845895  |         0.0507537   | no            |
|  8591.5 | mean_shift    | mahalanobis   |        0.7183 |             0.7727 |             0.5376 | recall    | 6.27554e-19 |         3.76533e-18 | **yes**       |
## ARI
|      U | algorithm 1   | algorithm 2   |   cliff_delta |   mean algorithm 1 |   mean algorithm 2 | measure   |     p-value |   p-value corrected | significant   |
|-------:|:--------------|:--------------|--------------:|-------------------:|-------------------:|:----------|------------:|--------------------:|:--------------|
| 3174   | agglomerative | birch         |       -0.3652 |             0.4162 |             0.4796 | ari       | 0.999996    |         5.99998     | no            |
| 2706   | agglomerative | kmeans        |       -0.4588 |             0.4162 |             0.5075 | ari       | 1           |         6           | no            |
| 2585.5 | agglomerative | mean_shift    |       -0.4829 |             0.4162 |             0.5173 | ari       | 1           |         6           | no            |
| 6826   | birch         | agglomerative |        0.3652 |             0.4796 |             0.4162 | ari       | 4.08652e-06 |         2.45191e-05 | **yes**       |
| 4096   | birch         | kmeans        |       -0.1808 |             0.4796 |             0.5075 | ari       | 0.986451    |         5.91871     | no            |
| 4140   | birch         | mean_shift    |       -0.172  |             0.4796 |             0.5173 | ari       | 0.98225     |         5.8935      | no            |
| 7294   | kmeans        | agglomerative |        0.4588 |             0.5075 |             0.4162 | ari       | 1.04706e-08 |         6.28235e-08 | **yes**       |
| 5904   | kmeans        | birch         |        0.1808 |             0.5075 |             0.4796 | ari       | 0.0136338   |         0.0818029   | no            |
| 4707.5 | kmeans        | mean_shift    |       -0.0585 |             0.5075 |             0.5173 | ari       | 0.762982    |         4.57789     | no            |
| 7414.5 | mean_shift    | agglomerative |        0.4829 |             0.5173 |             0.4162 | ari       | 1.83388e-09 |         1.10033e-08 | **yes**       |
| 5860   | mean_shift    | birch         |        0.172  |             0.5173 |             0.4796 | ari       | 0.0178571   |         0.107143    | no            |
| 5292.5 | mean_shift    | kmeans        |        0.0585 |             0.5173 |             0.5075 | ari       | 0.237774    |         1.42664     | no            |