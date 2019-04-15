# Week 7

## Progress
调研实现针对TSP的遗传算法的变种

#### Partially Mapped Crossover Operator (PMX)
PMX的思路即部分映射，从parent1中选取一部分直接对应地映射到子个体中，剩余部分尝试从parent2直接映射得到，如果出现重复，则遍历搜寻至可行解。

#### Order Crossover Operator (OX)
有序映射，在直接截取parent1的一部分基因序列的同时，剩余部分按保留parent2中基因的顺序的方式不重复地填充到子个体中。

#### Cycle Crossover Operator (CX)
循环映射，利用两个父个体构成的环路获取parent1的某一串子序列，并用parent2填充剩余的部分。

#### Modified Crossover Operator (MX)
与OX相似，但只选取一个截断点，保留了个体起止两端的特征。
