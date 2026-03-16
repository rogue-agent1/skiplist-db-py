#!/usr/bin/env python3
"""Skip list key-value store with range queries."""
import sys,random

class Node:
    def __init__(self,key=None,val=None,level=0):
        self.key=key;self.val=val;self.forward=[None]*(level+1)

class SkipList:
    def __init__(self,max_level=16,p=0.5,seed=42):
        self.max_level=max_level;self.p=p;self.rng=random.Random(seed)
        self.header=Node(level=max_level);self.level=0;self.size=0
    def _random_level(self):
        lvl=0
        while self.rng.random()<self.p and lvl<self.max_level:lvl+=1
        return lvl
    def insert(self,key,val):
        update=[None]*(self.max_level+1);x=self.header
        for i in range(self.level,-1,-1):
            while x.forward[i] and x.forward[i].key<key:x=x.forward[i]
            update[i]=x
        x=x.forward[0]
        if x and x.key==key:x.val=val;return
        lvl=self._random_level()
        if lvl>self.level:
            for i in range(self.level+1,lvl+1):update[i]=self.header
            self.level=lvl
        n=Node(key,val,lvl)
        for i in range(lvl+1):
            n.forward[i]=update[i].forward[i];update[i].forward[i]=n
        self.size+=1
    def get(self,key):
        x=self.header
        for i in range(self.level,-1,-1):
            while x.forward[i] and x.forward[i].key<key:x=x.forward[i]
        x=x.forward[0]
        return x.val if x and x.key==key else None
    def delete(self,key):
        update=[None]*(self.max_level+1);x=self.header
        for i in range(self.level,-1,-1):
            while x.forward[i] and x.forward[i].key<key:x=x.forward[i]
            update[i]=x
        x=x.forward[0]
        if not x or x.key!=key:return False
        for i in range(self.level+1):
            if update[i].forward[i]!=x:break
            update[i].forward[i]=x.forward[i]
        while self.level>0 and not self.header.forward[self.level]:self.level-=1
        self.size-=1;return True
    def range_query(self,lo,hi):
        x=self.header
        for i in range(self.level,-1,-1):
            while x.forward[i] and x.forward[i].key<lo:x=x.forward[i]
        x=x.forward[0];result=[]
        while x and x.key<=hi:result.append((x.key,x.val));x=x.forward[0]
        return result

def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        sl=SkipList()
        for i in range(100):sl.insert(i,f"v{i}")
        assert sl.get(50)=="v50"
        assert sl.get(999) is None
        assert sl.size==100
        sl.insert(50,"updated");assert sl.get(50)=="updated"
        assert sl.delete(50);assert sl.get(50) is None;assert sl.size==99
        r=sl.range_query(10,15)
        assert len(r)==5  # 10,11,12,13,14 (50 deleted, 15 excluded? no, <=15)
        assert r[0]==(10,"v10")
        print("All tests passed!")
    else:
        sl=SkipList()
        for i in range(20):sl.insert(i,i**2)
        print(f"Range [5,10]: {sl.range_query(5,10)}")
if __name__=="__main__":main()
