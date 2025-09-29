import multiprocessing
def is_prime(n):
    if n==0 or n==1:
        return False
    if n==2:
        return True
    i=2
    while i*i<=n:
        if n%i==0:
            return False
        i+=1
    return True

def fsum(start,end):
    return sum(n for n in range(start, end) if is_prime(n))

def main():
    start=1
    end=1000000
    pnum=10  # 分成10个子进程
    group=(end-start+1)//pnum  # 均分到10个子进程里的分组数目，即100000
    with multiprocessing.Pool(processes=pnum) as pool:
        results=[pool.apply_async(fsum,(i*group+start,(i+1)*group+start))for i in range(pnum)]
        total=sum(result.get() for result in results)
    print(f"1~1000000所有质数的和为：{total}")

if __name__ == "__main__":
    main()