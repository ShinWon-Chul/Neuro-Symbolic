# Knowledge Inference and Knowledge Completion Methods using Neuro-Symbolic Inductive Rules
해당 레파지토리는 [뉴로 심볼릭 유도 규칙을 활용한 지식 추론 및 지식 완성 방법](https://github.com/ShinWon-Chul/Neuro-Symbolic/blob/main/papers/%EB%89%B4%EB%A1%9C%20%EC%8B%AC%EB%B3%BC%EB%A6%AD%20%EA%B8%B0%EB%B0%98%20%EA%B7%9C%EC%B9%99%20%EC%9C%A0%EB%8F%84%20%EB%B0%8F%20%EC%B6%94%EB%A1%A0%20%EC%97%94%EC%A7%84%EC%9D%84%20%ED%99%9C%EC%9A%A9%ED%95%9C%20%EC%A7%80%EC%8B%9D%20%EC%99%84%EC%84%B1%20%EC%8B%9C%EC%8A%A4%ED%85%9C.pdf)를 구현한 것입니다.  
해당 코드는 지식 그래프와 규칙 템플릿을 입력으로 지식 그래프로부터 새로운 지식을 추론할 수 있는 규칙을 자동으로 유도하는 end-to-end leanring을 제공합니다.  
해당 코드에 대한 직관적인 파악은 [`papers/CSCI_NTP.pdf`](https://github.com/ShinWon-Chul/Neuro-Symbolic/blob/main/papers/CSCI_NTP.pdf)를 참조 하십시오.

## 데이터 형식
NTP의 데이터는 `.txt` 기본적으로 트리플(subject, relation, object)형식을 따릅니다.

```shell
NTP/data/example_8.txt
BART	nationality	USA
BART	birthPlace	NEWYORK
NEWYORK	locatedIn	USA
BART	hasFather	HOMER
BART	hasGrandfather	ABE
HOMER	hasParent	ABE
LISA	sibling	BART
BART	sibling	LISA
```

```shell
NTP/data/example_8.nlt
2	#1(X, Y) :- #2(X, Z),#3(Z, Y).
2	#1(X, Y) :- #2(Y, X).
```

- `*.txt` 파일은 *fact*를 나타냅니다. (example of a fact: `BART hasFather HOMER`)

- `*.nlt` 파일은 *rule templates*을 나타냅니다. (example of a rule template: `#1(X,Y) :- #2(X,Z), #3(Z,Y)`)

## 출력 예시
```shell
/NTP/out/example_8/example_8_rule.tsv
(('p0', 'X', 'Y'), ('p1', 'X', 'Z'), ('p2', 'Z', 'Y'))
0.819403	nationality(X,Y) :- birthPlace(X,Z), locatedIn(Z,Y)
0.74837		hasGrandfather(X,Y) :- hasFather(X,Z), hasParent(Z,Y)

(('p0', 'X', 'Y'), ('p1', 'Y', 'X'))
0.938703	sibling(X,Y) :- sibling(Y,X)
0.094027	sibling(X,Y) :- sibling(Y,X)
```



## Running

NTP를 실행하기 위한 기본 파일은 [`NTP/Neural Theorem Prover_v2.1.ipynb`](/NTP/Neural%20Theorem%20Prover_v2.1.ipynb) 입니다.