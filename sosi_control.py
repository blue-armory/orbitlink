import socket
import struct
import time
import argparse
import random
import threading
import json
from datetime import datetime
import os

def track_write():
    # Sample tracks taken from real world tracks on Rayday 202, 2023
    sample_tracks = [
    "1   116U 61015A   23201.86389281  .00000058  00000-0  10298-3 0  9990",
    "2   116  66.8114 329.4555 0081834 295.5649  63.6987 13.91929622149336",
    "1   117U 61015B   23202.13208364 -.00000000  00000-0  60128-4 0  9990",
    "2   117  66.8126  73.8558 0082342 316.9205  42.5447 13.89953919146881",
    "1   120U 61015E   23202.53485307  .00000704  00000-0  30670-3 0  9990",
    "2   120  66.7077 320.2435 0109104  50.0331 311.0284 14.26510765197175",
    "1   121U 61015F   23202.34961347  .00000074  00000-0  10040-3 0  9992",
    "2   121  66.7468 160.3321 0090282  22.5927 337.9091 13.99842991177706",
    "1   122U 61015G   23202.38445522  .00004525  00000-0  67007-3 0  9999",
    "2   122  66.7519 341.0073 0069399 324.9624  34.6940 14.74482636257190",
    "1   123U 61015H   23201.96867563  .00000622  00000-0  21695-3 0  9993",
    "2   123  66.6863  14.5088 0118252 324.1551  35.1655 14.38201692227124",
    "1   128U 61015N   23202.36700111  .00000062  00000-0  90105-4 0  9999",
    "2   128  66.6766 314.0380 0098396 323.1142  36.3199 14.01426445166678",
    "1   130U 61015Q   23201.84314111  .00000034  00000-0  75083-4 0  9992",
    "2   130  66.7723   5.4533 0090950 312.2146  47.1242 13.98915204163371",
    "1   132U 61015S   23202.15037454  .00000029  00000-0  78540-4 0  9996",
    "2   132  66.6604  76.4953 0076146 191.8416 168.0876 13.94452997156072",
    "1   133U 61015T   23201.88298126  .00000671  00000-0  34954-3 0  9994",
    "2   133  67.1163  33.2130 0061643 265.8167  93.5883 14.19483690182990",
    "1   134U 61015U   23202.20672286  .00000109  00000-0  12887-3 0  9992",
    "2   134  66.8800 140.2322 0088308 240.0716 119.1576 13.97099185157778",
    "1   136U 61015W   23202.23959762  .00001687  00000-0  59872-3 0  9991",
    "2   136  67.5295 124.8116 0060439 280.9344  78.4967 14.35659322204514",
    "1   141U 61015AB  23202.21184784  .00000305  00000-0  32045-3 0  9998",
    "2   141  66.5892 128.3870 0052396  13.0169 347.2244 13.87526790124762",
    "1   144U 61015AE  23202.25441279  .00000351  00000-0  34176-3 0  9998",
    "2   144  66.4996 134.0128 0048057 310.3649  49.3235 13.90554868137444",
    "1   147U 61015AH  23202.54648933  .00000940  00000-0  47159-3 0  9998",
    "2   147  66.6168 232.9741 0045737 101.1320 259.4920 14.20478244183952",
    "1   150U 61015AL  23202.43432882  .00000527  00000-0  55603-3 0  9998",
    "2   150  66.2497 359.0982 0058187 160.0409 200.2956 13.82013571962133",
    "1   152U 61015AN  23202.21264147  .00000458  00000-0  27401-3 0  9991",
    "2   152  66.5936 143.4364 0156265 201.0503 158.4108 14.09861149176279",
    "1   154U 61015AQ  23202.30863343  .00000215  00000-0  17835-3 0  9997",
    "2   154  66.6596 306.7356 0080659  18.9651 341.4407 14.05005127167808",
    "1   155U 61015AR  23202.49255582  .00001999  00000-0  62520-3 0  9999",
    "2   155  66.8775 222.1221 0044319 351.6088   8.4271 14.42169545207952",
    "1   159U 61015AV  23202.04535615  .00000174  00000-0  56053-3 0  9990",
    "2   159  65.5261  62.0370 0373169 205.0554 153.1948 13.02394675942994",
    "1   162U 61017A   23202.85370745  .00000112  00000-0  78421-4 0  9992",
    "2   162  47.8985 152.9974 0044306 172.7948 187.3590 14.44402778263560",
    "1   163U 61018A   23201.86864064  .00000016  00000-0  53646-2 0  9999",
    "2   163  91.1143 159.9230 0097288 242.1827 116.9158  8.91835520 19563",
    "1   177U 61015BB  23202.20199140  .00000459  00000-0  26985-3 0  9994",
    "2   177  66.6624  35.8016 0108101 115.1432 246.0918 14.13887478191550",
    "1   178U 61015BC  23202.09734651  .00000106  00000-0  13791-3 0  9994",
    "2   178  66.8656  75.8321 0075954  29.1385 331.3901 13.92572452149777",
    "1   188U 61018C   23201.84285167 -.00000005  00000-0 -24000-2 0  9997",
    "2   188  91.1063 162.5948 0127031  98.9949 262.5326  8.93824772 23603",
    "1   195U 61028D   23202.36762536  .00000007  00000-0  46180-2 0  9997",
    "2   195  95.8667 341.9953 0114391  20.8321 339.7141  8.65607723951510",
    "1   202U 61031A   23202.46858284  .00000061  00000-0  48819-4 0  9990",
    "2   202  32.4374 279.6033 0100999  70.6026 290.5480 13.63616735 76055",
    "1   204U 61031C   23202.46326819  .00000078  00000-0  65751-4 0  9998",
    "2   204  32.4438 346.6437 0098362 151.2470 209.3618 13.64938969 78274",
    "1   205U 61031B   23202.02951510  .00000059  00000-0  43698-4 0  9998",
    "2   205  32.4422  66.7716 0102292 202.5698 157.0402 13.62461250 74614",
    "1   210U 61015BE  23202.11452066  .00000586  00000-0  56052-3 0  9990",
    "2   210  66.4577 102.7880 0055046 261.6077  97.8755 13.86959647118396",
    "1   223U 61015BK  23201.99125635 -.00000015  00000-0  49557-4 0  9999",
    "2   223  66.8914  17.3435 0068100 356.7883   3.2749 13.88755644143779",
    "1   224U 61015BL  23202.79670351  .00000908  00000-0  55963-3 0  9996",
    "2   224  66.7379 318.6752 0058243  58.8023  19.7942 14.09174335163210",
    "1   225U 61015BM  23202.26351024  .00001772  00000-0  62945-3 0  9990",
    "2   225  66.7988 161.4661 0114767 293.2771  65.6282 14.33094243205703",
    "1   226U 62002A   23201.95597625  .00000116  00000-0  77649-4 0  9991",
    "2   226  48.2957 135.4340 0077606 198.0278 161.7865 14.46065451235536",
    "1   227U 62002B   23202.64764726  .00000491  00000-0  19423-3 0  9998",
    "2   227  48.1479  73.6792 0130811   8.2855 352.0159 14.38897941212107",
    "1   228U 62002C   23201.77859392  .00006836  00000-0  46004-3 0  9990",
    "2   228  48.4283 338.6253 0013523 286.6516  73.2926 15.07577631305066",
    "1   230U 61015BN  23202.29718456  .00000064  00000-0  98290-4 0  9991",
    "2   230  66.8834 138.2297 0098546 221.7860 137.5669 13.96312810157972",
    "1   232U 61015BQ  23202.33919131  .00000257  00000-0  22604-3 0  9990",
    "2   232  66.8224 325.2692 0054260 148.7438 211.6891 13.99723287158810",
    "1   234U 61015BS  23202.18003361  .00000398  00000-0  30066-3 0  9991",
    "2   234  66.8768 281.4676 0072480 187.5208 172.4797 14.02776060162940",
    "1   235U 61015BT  23202.01776800  .00000451  00000-0  26979-3 0  9997",
    "2   235  66.9558  54.8292 0158309  52.7005 308.8395 14.09422816172010",
    "1   245U 61015CA  23202.04409580  .00001287  00000-0  70138-3 0  9993",
    "2   245  66.1034  75.6841 0042299 102.5560 258.0262 14.15099604177828",
    "1   246U 61015CB  23202.72371462 -.00000009  00000-0  56732-4 0  9993",
    "2   246  66.8673 235.6286 0064195 168.0672 192.1944 13.85896226477241",
    "1   252U 61015CD  23202.28987331  .00000283  00000-0  35572-3 0  9990",
    "2   252  67.0771 172.2076 0061905 261.6425 165.1765 13.76717866105561",
    "1   261U 61015CH  23202.38433276  .00000220  00000-0  19518-3 0  9998",
    "2   261  66.6799 180.9458 0091265 337.9847  21.7325 14.00247415163382",
    "1   262U 61015CJ  23202.66566477  .00004437  00000-0  12351-2 0  9991",
    "2   262  66.4649  96.4458 0066378 112.2530 248.5632 14.45993045204782",
    "1   264U 61015CL  23202.34224620  .00002711  00000-0  10775-2 0  9990",
    "2   264  66.5272 171.7654 0018870  23.1835 337.0108 14.30142055181781",
    "1   268U 61015CN  23201.87075990  .00000040  00000-0  25877-3 0  9998",
    "2   268  67.9410 354.8682 0654767 194.9996 321.6633 12.50915849820786",
    "1   274U 62010D   23201.80883877  .00000006  00000-0  30324-3 0  9990",
    "2   274  86.6569 127.7099 0363955  25.4421 336.3921  9.39405523101424",
    "1   309U 62025A   23202.31281190  .00000318  00000-0  90196-4 0  9992",
    "2   309  58.0910 155.2712 0185473 243.7686 114.4175 14.57834548226826",
    "1   312U 62025C   23202.73085945  .00000564  00000-0  13161-3 0  9991",
    "2   312  58.2491 301.5680 0203163 331.6512  27.3578 14.56204078204416",
    "1   324U 61015DA  23202.07128501  .00000869  00000-0  51728-3 0  9994",
    "2   324  66.8646 191.7729 0060597  91.5972 269.2060 14.11133388173507",
    "1   325U 61015DB  23202.71147703  .00001100  00000-0  55152-3 0  9995",
    "2   325  66.9165 297.8916 0052305 120.1548 240.4744 14.19566466182692",
    "1   327U 61015DD  23202.21377441  .00000231  00000-0  23952-3 0  9993",
    "2   327  66.5432 126.9918 0105590 101.2237 260.0729 13.90046704139588",
    "1   329U 61015DF  23202.83122289  .00000053  00000-0  14641-3 0  9998",
    "2   329  66.7821 341.1180 0117145 337.9701 173.5668 13.65554678 85530",
    "1   330U 61015DG  23202.02831847  .00000834  00000-0  57301-3 0  9995",
    "2   330  66.9806  61.1034 0055266 203.3761 156.4813 14.03588259147964",
    "1   333U 61015DK  23202.24249011  .00003574  00000-0  71350-3 0  9992",
    "2   333  66.7102 244.4430 0046229  18.3143 341.9623 14.62454120232911",
    "1   334U 61015DL  23202.54460449  .00000013  00000-0  68320-4 0  9995",
    "2   334  66.9227 246.4625 0076562 154.4088 206.0814 13.91413482148784",
    "1   335U 61015DM  23202.34886545  .00001037  00000-0  53160-3 0  9995",
    "2   335  66.8431 330.8510 0047506 241.8271 117.8019 14.18797200176840",
    "1   336U 61015DN  23202.25213375  .00000104  00000-0  19915-3 0  9995",
    "2   336  67.0300 149.5039 0078787 180.8759 251.2736 13.68685909 94392",
    "1   337U 61015DP  23202.17910581  .00000486  00000-0  55963-3 0  9996",
    "2   337  67.0083 269.0775 0109038 301.5529  57.4931 13.75056749 99083",
    "1   350U 61015DQ  23202.64041662  .00000277  00000-0  15051-3 0  9990",
    "2   350  66.9127  67.7064 0133309 235.3375 123.5098 14.21231201212569",
    "1   369U 62039A   23202.32215055  .00002509  00000-0  27500-3 0  9993",
    "2   369  98.5349 190.4409 0087827 327.8711  31.7167 14.86036412257998",
    "1   402U 61015EB  23202.12430882  .00004131  00000-0  11665-2 0  9996",
    "2   402  66.6620 269.9305 0032713   7.7736 352.3870 14.46327325186677",
    "1   406U 61015EF  23202.76637101  .00000295  00000-0  41412-3 0  9994",
    "2   406  66.7800 332.7835 0115300  23.3409 125.1416 13.67755236 76379",
    "1   407U 61015EG  23202.59554578  .00008889  00000-0  18956-2 0  9995",
    "2   407  66.3248 265.3832 0082530 275.7702 157.1963 14.57189441175604",
    "1   408U 61015EH  23202.15653101  .00000337  00000-0  41994-3 0  9999",
    "2   408  66.7866 121.7484 0061468 127.3498 300.6818 13.75639115160036",
    "1   414U 61015EP  23202.34075325  .00000053  00000-0  12964-3 0  9993",
    "2   414  66.4437 158.1678 0042266  37.5537  39.4782 13.77236896116347",
    "1   416U 61015ER  23202.16376603  .00000756  00000-0  43754-3 0  9999",
    "2   416  66.5216 122.8868 0074134 169.6371 190.6267 14.13050242182088",
    "1   463U 61015EZ  23202.01655633  .00002624  00000-0  74164-3 0  9993",
    "2   463  66.7715  40.3637 0054954 338.7221  21.1601 14.46323648215452",
    "1   467U 61015FD  23202.55662021  .00001842  00000-0  23696-2 0  9999",
    "2   467  66.5594  32.6738 0258884 249.8002 107.5044 13.51746355137511",
    "1   470U 61015FG  23202.20330251  .00000456  00000-0  31796-3 0  9993",
    "2   470  66.2307 123.5760 0077397 248.8220 110.4580 14.06486802163356",
    "1   474U 61015FL  23202.25996204  .00037047  00000-0  27926-2 0  9993",
    "2   474  66.2400 125.8548 0019048 212.0527 311.1747 15.02140451233992",
    "1   506U 62070A   23202.22643554 -.00000028  00000-0  75269-4 0  9990",
    "2   506  52.0034 130.1903 0276601 283.7424  73.2854 13.85336447 61972",
    "1   530U 61015FU  23202.62199634  .00000176  00000-0  17125-3 0  9993",
    "2   530  66.8798  66.7723 0084660 220.2363 139.2435 13.98613444159653",
    "1   537U 61015FW  23202.54470244  .00000454  00000-0  59663-3 0  9992",
    "2   537  67.2269  35.1068 0173565   1.9835  28.8838 13.63532883870852",
    "1   545U 61015GE  23202.43753290  .00000337  00000-0  42750-3 0  9993",
    "2   545  67.2303 216.0434 0155209 132.5499 228.8797 13.69635890 85390",
    "1   548U 61015GH  23202.52447288  .00002302  00000-0  38825-3 0  9995",
    "2   548  66.6735  40.3625 0116743 214.3861 144.9663 14.67111045268424",
    "1   549U 61015GJ  23202.17753674  .00000072  00000-0  23771-3 0  9992",
    "2   549  66.6947 109.6747 0221453 264.0707 250.8312 13.35989295 21407",
    "1   552U 61015GM  23202.00895987  .00001520  00000-0  11344-2 0  9993",
    "2   552  67.7393  52.0000 0114284 224.6980 134.4855 13.94193303108732",
    "1   553U 63004A   23201.89165647 -.00000107  00000-0  00000+0 0  9998",
    "2   553  28.9171 294.2543 0756761 167.5599 194.4843  1.16484327222416",
    "1   558U 61015GQ  23201.61308093  .00000116  00000-0  44849-3 0  9999",
    "2   558  65.6979 265.9606 0472447 165.3611 315.9541 12.86012461913368",
    "1   559U 61015GR  23202.37506301  .00006191  00000-0  15716-2 0  9995",
    "2   559  66.6093 344.9367 0071970 227.3503 132.1526 14.49849600195104",
    "1   575U 63013B   23202.40068718 -.00000051  00000-0 -59891-3 0  9996",
    "2   575  42.7730 329.1174 4008061 359.0852  15.5564  6.40244171408197",
    "1   589U 63014D   23202.24328680 -.00000041  00000-0 -20169-1 0  9994",
    "2   589  87.3094 292.1421 0162302  10.1163 350.2899  8.65642650902225",
    "1   602U 63014E   23202.24808141 -.00000011  00000-0 -63180-2 0  9993",
    "2   602  87.3240 291.2041 0053351  37.8764 322.5828  8.67231585906061",
    "1   630U 63030C   23202.61173618  .00000006  00000-0  16722-2 0  9999",
    "2   630  88.3853 262.0124 0030169 265.3460  94.3946  8.59853213883860",
    "1   644U 61015GV  23202.05624420  .00000710  00000-0  98763-3 0  9993",
    "2   644  67.0957 209.3491 0146198 160.3982 234.2315 13.58992793 53729",
    "1   645U 61015GW  23202.31681809 -.00000116  00000-0 -11338-3 0  9992",
    "2   645  66.5911 323.1503 0409265  11.1111  14.9391 13.03966194941760",
    "1   649U 61015HA  23202.32521933  .00000061  00000-0  34486-3 0  9994",
    "2   649  66.2657 147.3465 0562787 191.4548 336.1455 12.64786151858818",
    "1   652U 61015HD  23202.70870363  .00001454  00000-0  82028-3 0  9996",
    "2   652  66.6946 297.5863 0075614  22.3208 338.1142 14.11685571144035",
    "1   655U 61015HG  23202.28484359  .00000225  00000-0  60289-3 0  9998",
    "2   655  67.2580 295.3047 0368332 326.2351  62.3924 13.08311363948414",
    "1   659U 61015HL  23201.90215014  .00000498  00000-0  14730-2 0  9991",
    "2   659  67.1642   7.0019 0591786 228.8835 289.9713 12.65944556856518",
    "1   660U 61015HM  23201.90276801  .00008165  00000-0  14391-2 0  9996",
    "2   660  66.5216   0.1992 0048339 257.3478 179.8854 14.67220140227914",
    "1   669U 63038A   23202.31053466  .00000052  00000-0  71373-4 0  9990",
    "2   669  90.0162 334.8481 0024414 285.4483  91.1171 13.46030003937314",
    "1   670U 63038B   23201.99510622  .00000082  00000-0  12398-3 0  9991",
    "2   670  90.0062 334.6412 0041174 192.5498 167.4628 13.44450158932058",
    "1   671U 63038C   23201.81431224  .00000089  00000-0  13387-3 0  9999",
    "2   671  90.0071 334.6546 0041310 151.9652 208.3733 13.44976397932803",
    "1   701U 63047G   23202.68879754  .00000678  00000-0  20567-3 0  9995",
    "2   701  30.0154 351.8390 0523894 313.6011  42.2224 13.78510521963768",
    "1   705U 63049C   23201.69179927  .00000107  00000-0  15787-3 0  9991",
    "2   705  89.9087  79.5591 0035810  72.8025 346.7143 13.47448959929565",
    "1   706U 63049D   23202.60784796  .00000283  00000-0  39207-3 0  9998",
    "2   706  89.9088  82.6623 0025885 284.7098 104.6534 13.55772685939878",
    "1   716U 63054A   23201.86014707  .00000666  00000-0  13935-3 0  9995",
    "2   716  58.4965   4.2764 0020715 346.5184  13.5298 14.70413569180391",
    "1   720U 63054C   23202.36525991  .00001000  00000-0  28978-3 0  9994",
    "2   720  58.4736 320.6678 0112279 164.3650 196.0892 14.48010096127528",
    "1   727U 64001A   23202.06025256  .00000048  00000-0  74591-4 0  9994",
    "2   727  69.9064  50.0093 0015033 323.1750  36.8321 13.95508186 29428",
    "1   728U 64001B   23202.42798892  .00000091  00000-0  10296-3 0  9997",
    "2   728  69.9094 329.4767 0016061 274.2463  85.6807 13.97349047 31797",
    "1   730U 64001D   23202.00666994  .00000033  00000-0  63693-4 0  9997",
    "2   730  69.9065  37.5238 0015710 310.5113 124.8725 13.95756626912992",
    "1   731U 64001E   23201.95830153  .00000049  00000-0  74907-4 0  9998",
    "2   731  69.9064  28.7611 0015886 307.0183  52.9468 13.95988685 29795",
    "1   732U 63053H   23202.66900967  .00003980  00000-0  14917-2 0  9995",
    "2   732  78.5750 100.7704 0482897 208.4210 148.9819 13.82418512846328",
    "1   733U 64002A   23201.76859079  .00000296  00000-0  12532-3 0  9997",
    "2   733  99.0252 151.4229 0033457 180.5681 179.5469 14.32835995100783",
    "1   734U 64002B   23202.64849165  .00000126  00000-0  68305-4 0  9993",
    "2   734  99.0307  83.8926 0015133  30.2283 329.9767 14.29085745 97207",
    "1   735U 64002C   23202.27912227  .00000108  00000-0  62626-4 0  9993",
    "2   735  99.0564  78.1003 0017263 137.9984 222.2523 14.28024119 95193",
    "1   738U 64003B   23202.67952180 -.00000010  00000-0  00000+0 0  9999",
    "2   738  46.4633 108.7545 2600876 263.7738  66.3645  7.39351261607225",
    "1   739U 63047H   23202.73894268  .00001204  00000-0  19179-3 0  9992",
    "2   739  30.4241   6.4821 0643595 105.4467 261.8109 13.83224746994262"
    ]
    # Draw a random number of TLE's between 3-20
    payload_start = random.randrange(0, len(sample_tracks)-20)
    payload_end = payload_start + random.randrange(3, 19)
    payload = sample_tracks[payload_start:payload_end]

    # Ensure that a full TLE is captured with each broadcast (remove any orphaned first/second lines)
    if payload:
        last_tle = payload[-1]
        first_tle = payload[0]
        if last_tle.startswith("1"):
            payload.pop()
        
        if first_tle.startswith("2"):
            payload.pop(0)
        

    # Define packet variables
    source_address = '127.0.0.1'
    destination_address = '127.0.0.1'
    protocol_id = random.randint(0,255)  # UDP protocol ID
    sequence_number = random.randint(0,255) # Must fall within Header range
    timestamp = int(time.time())  # Current Unix timestamp

    # Create a socket and bind to the source address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((source_address, 0))  # Bind to a random free port

    # Send the packet with the header and payload
    payload = "\n".join(payload)
    payload = payload.encode()
    payload_length = len(payload)

    # Pack the header fields into a binary string
    HEADER_FORMAT = '!4s4sBBIH'
    header = struct.pack(HEADER_FORMAT, socket.inet_aton(source_address), socket.inet_aton(destination_address), protocol_id, sequence_number, timestamp, payload_length)
    s.sendto(header + payload, (destination_address, 7073))  # Use a random destination port

    # Close the socket
    s.close()

def track_store(stop_event):
    host = "0.0.0.0"  # Listen on all available network interfaces
    port = 7073
    HEADER_FORMAT = '!4s4sBBIH'
    header_length = struct.calcsize(HEADER_FORMAT)
    
    # Create a socket object and bind it to the specified host and port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port)) 

    print(f"Listening for UDP traffic on port {port}...")

    # Continuously listen for incoming UDP traffic
    try:
        while not stop_event.is_set():
            try:
                # Receive up to 4096 bytes of data from the client
                data, addr = sock.recvfrom(4096)

                # Unpack the header
                header_data = data[:header_length]
                src_ip, dest_ip, protocol_id, sequence_number, timestamp, payload_length = struct.unpack(HEADER_FORMAT, header_data)

                # Extract and decode the payload as UTF-8
                payload_data = data[header_length:header_length+payload_length]
                payload_text = payload_data.decode('utf-8')

                # Prepare the data for JSON
                record = {
                    'src_ip': socket.inet_ntoa(src_ip),
                    'dest_ip': socket.inet_ntoa(dest_ip),
                    'protocol_id': protocol_id,
                    'sequence_number': sequence_number,
                    # Convert from epoch time
                    'timestamp': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                    'payload': payload_text,
                }

                # Write the data to sosi_store.tle
                with open('sosi_store.tle', 'a') as file:
                    json.dump(record, file)
                    file.write('\n')
            except OSError as e:
                print(f"Error while receiving data: {e}")

    except KeyboardInterrupt:
        pass
    finally:
        # Close the socket
        sock.close()
        print("Listener thread stopped.")

def queue_write():
    #TODO Placeholder for main, add argparse variables
    destination_ip = '127.0.0.1'
    PORT = '7073'

    # Read top 1-5 number of entries in sosi_store.tle
    MAX_ENTRIES = 5
    FILENAME = 'sosi_store.tle'
    entries = []
    remaining_entries = []
    try:
        with open(FILENAME, 'r') as json_file:
            for i, line in enumerate(json_file):
                entry = json.loads(line.strip())
                if i < MAX_ENTRIES:
                    entries.append(entry)
                else:
                    remaining_entries.append(line)
    except FileNotFoundError:
        print(f"{FILENAME} not found. Nothing to read.")
        return

    # Remove those entries from sosi_store.tle file
    with open(FILENAME, 'w') as json_file:
        json_file.writelines(remaining_entries)

    # Send entries via UDP socket to main on port 8067
    if entries:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            for entry in entries:
                data = json.dumps(entry).encode('utf-8')
                s.sendto(data, (destination_ip, PORT))
        finally:
            s.close()


if __name__ == '__main__':
    #TODO Initialize Menu
    
    # Define the packet header fields
    source_address = '127.0.0.1'
    destination_address = '127.0.0.1' # TestWinxp: 192.168.138.234
    
    # Create an Event object to signal the listener thread to stop
    stop_event = threading.Event()

    # Start listener in a background thread
    listener_thread = threading.Thread(target=track_store, args=(stop_event,))
    listener_thread.start()

    # Start track writer
    #TODO Add interval argument and send tracks at a specified interval by re-running track_write() function in a loop
    try:
        time.sleep(5)
        track_write()
        time.sleep(5)
        queue_write()
    except KeyboardInterrupt:
        pass
    finally:
        # Give the thread some time to finish its work
        stop_event.set()
        time.sleep(1)
        print("Terminating the program...")
        os._exit(1)
        

