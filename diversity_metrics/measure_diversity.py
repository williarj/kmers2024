import pandas as pd
import sys
import numpy as np
import mmh3
from sklearn.metrics.pairwise import cosine_similarity

id = int(sys.argv[1])
k_len = float(sys.argv[2])
coverage = int(sys.argv[3])
num_ind = int(sys.argv[4])
kmer_folder = sys.argv[5]
output = sys.argv[6]

def CalcBCTwoIndividuals(df1,df2,df_inter):
    print("Calculating bray-curtis...")
    # df1 = pd.read_csv(file1,sep="\t",header=None,names=["kmer","counts"])
    sum1 = sum(df1.counts)

    # df2 = pd.read_csv(file2,sep="\t",header=None,names=["kmer","counts"])
    sum2 = sum(df2.counts)

    sum_inter = sum(df_inter.counts)

    BC = 1 - (2*sum_inter/(sum1 + sum2))

    return BC

def CalcBFTwoIndividuals(df1,df2,h,size):
    print("Calculating counting bloom filter...")

    num_hash = h
    total = df1.shape[0]
    array_size = size

    array1 = np.zeros(array_size,dtype=np.int16)
    array2 = np.zeros(array_size,dtype=np.int16)

    kmers1 = df1.kmer
    counts1 = df1.counts
    total = df1.shape[0]

    for i in range(0,total):
        for k in range(0, num_hash):
            index = mmh3.hash(kmers1[i],k,signed=False)%array_size
            array1[index] += counts1[i]

    kmers2 = df2.kmer
    counts2 = df2.counts
    total = df2.shape[0]

    for i in range(0,total):
        for k in range(0, num_hash):
            index = mmh3.hash(kmers2[i],k,signed=False)%array_size
            array2[index] += counts2[i]

    # print("Calculating..")

    cosine = cosine_similarity([array1],[array2])

    return 1 - cosine[0][0]

def CalcCSTwoIndividuals(d1,d2):
    print("Calculate cosine similarity...")
    df1 = d1.set_index('kmer',inplace=False)
    df2 = d2.set_index('kmer',inplace=False)

    res = pd.concat([df1,df2],axis=1)
    res = res.fillna(0)
    array1 = res.iloc[:,0].values
    array2 = res.iloc[:,1].values
    CS = cosine_similarity([array1],[array2])

    return 1 - CS[0][0]

def update_write_file(score,m):
    print("Writing...")
    f = open(output,"a")
    # id,coverage,k-length,metric,score
    f.write(str(id) + "," +str(coverage) + "," + str(k_len) + "," + m + "," + str(score) + "\n")
    f.close()

pair = range(0,num_ind)

measure_names = ["BC","BF","CS"]
total_measures = [0,0,0]
total_pairs = 0
k_count_minimum = 5

for i in pair:
    for j in pair:
        if(i < j):
            file1 = kmer_folder + "n" + str(i) + ".txt"
            df1 = pd.read_csv(file1,sep="\t",header=None,names=["kmer","counts"])
            file2 = kmer_folder + "n" + str(j) + ".txt"
            df2 = pd.read_csv(file2,sep="\t",header=None,names=["kmer","counts"])
            inter_file = kmer_folder + "n" + str(i) + "_inter_n" + str(j) +  ".txt"
            df_inter = pd.read_csv(inter_file,sep="\t",header=None,names=["kmer","counts"])

            df1 = df1[df1['counts'] >= k_count_minimum].reset_index().drop("index",axis=1)
            df2 = df2[df2['counts'] >= k_count_minimum].reset_index().drop("index",axis=1)
            df_inter1 = df_inter[df_inter['counts'] >= k_count_minimum].reset_index().drop("index",axis=1)

            # [MODIFY HERE]
            # Here you can adjust the measure, and for the bloom filter adjust the number of hash functions
            # as well as array size. Just add to the total_measures array any combination of measures.
            # The original writes the results of bray-curtis, CBF with 4 hashes and 10000 bit arrays, and the cosine
            # dissimilarity on the raw k-mer count.

            total_measures[0] += CalcBCTwoIndividuals(df1,df2,df_inter)
            total_measures[1] += CalcBFTwoIndividuals(df1,df2,4,10000) # Last two variables are number of hash functions and array size, respectively
            total_measures[2] += CalcCSTwoIndividuals(df1,df2)

            total_pairs += 1

scores = np.divide(total_measures,total_pairs)
for r in range (0,len(measure_names)):
    update_write_file(scores[r],measure_names[r])
