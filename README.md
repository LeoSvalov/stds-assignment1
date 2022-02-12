## Statistical Techniques for Data Science. Assignment 1
#### Lev Svalov, DS-02. Innopolis University, Spring 2022
<hr>

Intro words:
Initially, I have picked Lin-SW algorithm for imlementation, but got stuck with understanding how the merge of buckets of summary elements works. Since GK-01 algorithm was needed for correct work of Lin-SW, I have accmplished its implementation and present it there. ;(

### GK-01 algorithm
The basic idea is that when N increases, the set of -approximate answers for querying φ-quantile expands as well, so correctness can be retained even if removing some elements. <br>
The implementation of the algorithm you can find in my repository using this [link](https://github.com/LeoSvalov/stds-assignment1).

### Comparison result:

![](https://i.imgur.com/vjvW9qa.png)

Detailed usage review can be found in .ipynb file in the repository.


#### References:
1. Chen Z., Zhang A. A survey of approximate quantile computation on large-scale data //IEEE Access. – 2020. – Т. 8. – С. 34585-34597.
2. Implemetation of algorithm. 
Github repository: https://github.com/LeoSvalov/stds-assignment1
    

