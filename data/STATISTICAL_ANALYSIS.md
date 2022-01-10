# Statistical Evaluation of Techniques
## MCC
|       U | algorithm 1   | algorithm 2   |   cliff_delta |   mean algorithm 1 |   mean algorithm 2 | measure   |     p-value |   p-value corrected | significant   |
|--------:|:--------------|:--------------|--------------:|-------------------:|-------------------:|:----------|------------:|--------------------:|:--------------|
|     0   | agglomerative | iqr           |       -1      |             0.4939 |             0.7952 | mcc       | 1           |         4           | no            |
|  2362   | agglomerative | kmeans        |       -0.5276 |             0.4939 |             0.5878 | mcc       | 1           |         4           | no            |
|  1218.5 | agglomerative | mahalanobis   |       -0.7563 |             0.4939 |             0.6034 | mcc       | 1           |         4           | no            |
| 10000   | iqr           | agglomerative |        1      |             0.7952 |             0.4939 | mcc       | 1.2733e-34  |         5.0932e-34  | **yes**       |
| 10000   | iqr           | kmeans        |        1      |             0.7952 |             0.5878 | mcc       | 1.27431e-34 |         5.09722e-34 | **yes**       |
| 10000   | iqr           | mahalanobis   |        1      |             0.7952 |             0.6034 | mcc       | 1.26843e-34 |         5.07373e-34 | **yes**       |
|  7638   | kmeans        | agglomerative |        0.5276 |             0.5878 |             0.4939 | mcc       | 5.79787e-11 |         2.31915e-10 | **yes**       |
|     0   | kmeans        | iqr           |       -1      |             0.5878 |             0.7952 | mcc       | 1           |         4           | no            |
|  4723.5 | kmeans        | mahalanobis   |       -0.0553 |             0.5878 |             0.6034 | mcc       | 0.750748    |         3.00299     | no            |
|  8781.5 | mahalanobis   | agglomerative |        0.7563 |             0.6034 |             0.4939 | mcc       | 1.24578e-20 |         4.98313e-20 | **yes**       |
|     0   | mahalanobis   | iqr           |       -1      |             0.6034 |             0.7952 | mcc       | 1           |         4           | no            |
|  5276.5 | mahalanobis   | kmeans        |        0.0553 |             0.6034 |             0.5878 | mcc       | 0.250028    |         1.00011     | no            |
## F1
|       U | algorithm 1   | algorithm 2   |   cliff_delta |   mean algorithm 1 |   mean algorithm 2 | measure   |     p-value |   p-value corrected | significant   |
|--------:|:--------------|:--------------|--------------:|-------------------:|-------------------:|:----------|------------:|--------------------:|:--------------|
|     0   | agglomerative | iqr           |       -1      |             0.5189 |             0.8058 | f1        | 1           |         4           | no            |
|  2952   | agglomerative | kmeans        |       -0.4096 |             0.5189 |             0.6112 | f1        | 1           |         4           | no            |
|  2303.5 | agglomerative | mahalanobis   |       -0.5393 |             0.5189 |             0.6285 | f1        | 1           |         4           | no            |
| 10000   | iqr           | agglomerative |        1      |             0.8058 |             0.5189 | f1        | 1.16585e-34 |         4.6634e-34  | **yes**       |
|  9971   | iqr           | kmeans        |        0.9942 |             0.8058 |             0.6112 | f1        | 2.78857e-34 |         1.11543e-33 | **yes**       |
| 10000   | iqr           | mahalanobis   |        1      |             0.8058 |             0.6285 | f1        | 1.07683e-34 |         4.30734e-34 | **yes**       |
|  7048   | kmeans        | agglomerative |        0.4096 |             0.6112 |             0.5189 | f1        | 2.79851e-07 |         1.1194e-06  | **yes**       |
|    29   | kmeans        | iqr           |       -0.9942 |             0.6112 |             0.8058 | f1        | 1           |         4           | no            |
|  5400.5 | kmeans        | mahalanobis   |        0.0801 |             0.6112 |             0.6285 | f1        | 0.163896    |         0.655584    | no            |
|  7696.5 | mahalanobis   | agglomerative |        0.5393 |             0.6285 |             0.5189 | f1        | 2.11111e-11 |         8.44445e-11 | **yes**       |
|     0   | mahalanobis   | iqr           |       -1      |             0.6285 |             0.8058 | f1        | 1           |         4           | no            |
|  4599.5 | mahalanobis   | kmeans        |       -0.0801 |             0.6285 |             0.6112 | f1        | 0.836708    |         3.34683     | no            |
## PRECISION
|      U | algorithm 1   | algorithm 2   |   cliff_delta |   mean algorithm 1 |   mean algorithm 2 | measure   |     p-value |   p-value corrected | significant   |
|-------:|:--------------|:--------------|--------------:|-------------------:|-------------------:|:----------|------------:|--------------------:|:--------------|
| 2972   | agglomerative | iqr           |       -0.4056 |             0.6569 |             0.682  | precision | 1           |         4           | no            |
| 2970.5 | agglomerative | kmeans        |       -0.4059 |             0.6569 |             0.7319 | precision | 1           |         4           | no            |
| 1318.5 | agglomerative | mahalanobis   |       -0.7363 |             0.6569 |             0.7655 | precision | 1           |         4           | no            |
| 7028   | iqr           | agglomerative |        0.4056 |             0.682  |             0.6569 | precision | 3.41527e-07 |         1.36611e-06 | **yes**       |
| 3482.5 | iqr           | kmeans        |       -0.3035 |             0.682  |             0.7319 | precision | 0.999897    |         3.99959     | no            |
| 1708   | iqr           | mahalanobis   |       -0.6584 |             0.682  |             0.7655 | precision | 1           |         4           | no            |
| 7029.5 | kmeans        | agglomerative |        0.4059 |             0.7319 |             0.6569 | precision | 3.38141e-07 |         1.35256e-06 | **yes**       |
| 6517.5 | kmeans        | iqr           |        0.3035 |             0.7319 |             0.682  | precision | 0.000104146 |         0.000416584 | **yes**       |
| 4181   | kmeans        | mahalanobis   |       -0.1638 |             0.7319 |             0.7655 | precision | 0.977582    |         3.91033     | no            |
| 8681.5 | mahalanobis   | agglomerative |        0.7363 |             0.7655 |             0.6569 | precision | 9.4794e-20  |         3.79176e-19 | **yes**       |
| 8292   | mahalanobis   | iqr           |        0.6584 |             0.7655 |             0.682  | precision | 3.72467e-16 |         1.48987e-15 | **yes**       |
| 5819   | mahalanobis   | kmeans        |        0.1638 |             0.7655 |             0.7319 | precision | 0.0225485   |         0.0901941   | no            |
## RECALL
|       U | algorithm 1   | algorithm 2   |   cliff_delta |   mean algorithm 1 |   mean algorithm 2 | measure   |     p-value |   p-value corrected | significant   |
|--------:|:--------------|:--------------|--------------:|-------------------:|-------------------:|:----------|------------:|--------------------:|:--------------|
|     0   | agglomerative | iqr           |       -1      |             0.4928 |             0.9896 | recall    | 1           |         4           | no            |
|  3961   | agglomerative | kmeans        |       -0.2078 |             0.4928 |             0.5672 | recall    | 0.99452     |         3.97808     | no            |
|  5643   | agglomerative | mahalanobis   |        0.1286 |             0.4928 |             0.5376 | recall    | 0.0571981   |         0.228792    | no            |
| 10000   | iqr           | agglomerative |        1      |             0.9896 |             0.4928 | recall    | 1.20453e-36 |         4.81812e-36 | **yes**       |
| 10000   | iqr           | kmeans        |        1      |             0.9896 |             0.5672 | recall    | 1.31127e-36 |         5.24508e-36 | **yes**       |
| 10000   | iqr           | mahalanobis   |        1      |             0.9896 |             0.5376 | recall    | 1.06799e-36 |         4.27197e-36 | **yes**       |
|  6039   | kmeans        | agglomerative |        0.2078 |             0.5672 |             0.4928 | recall    | 0.00551898  |         0.0220759   | no            |
|     0   | kmeans        | iqr           |       -1      |             0.5672 |             0.9896 | recall    | 1           |         4           | no            |
|  6602.5 | kmeans        | mahalanobis   |        0.3205 |             0.5672 |             0.5376 | recall    | 4.37403e-05 |         0.000174961 | **yes**       |
|  4357   | mahalanobis   | agglomerative |       -0.1286 |             0.5376 |             0.4928 | recall    | 0.943083    |         3.77233     | no            |
|     0   | mahalanobis   | iqr           |       -1      |             0.5376 |             0.9896 | recall    | 1           |         4           | no            |
|  3397.5 | mahalanobis   | kmeans        |       -0.3205 |             0.5376 |             0.5672 | recall    | 0.999957    |         3.99983     | no            |
## ARI
|    U | algorithm 1   | algorithm 2   |   cliff_delta |   mean algorithm 1 |   mean algorithm 2 | measure   |     p-value |   p-value corrected | significant   |
|-----:|:--------------|:--------------|--------------:|-------------------:|-------------------:|:----------|------------:|--------------------:|:--------------|
| 2936 | agglomerative | kmeans        |       -0.4128 |             0.4205 |             0.5093 | ari       | 1           |          4          | no            |
| 7064 | kmeans        | agglomerative |        0.4128 |             0.5093 |             0.4205 | ari       | 2.30338e-07 |          9.2135e-07 | **yes**       |