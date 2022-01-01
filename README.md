# Knowledge Inference and Knowledge Completion Methods using Neuro-Symbolic Inductive Rules
해당 레파지토리는 [뉴로 심볼릭 유도 규칙을 활용한 지식 추론 및 지식 완성 방법](http://oasis.dcollection.net/public_resource/pdf/200000491588_20211109213038.pdf)를 구현한 것입니다.  
해당 코드는 지식 그래프와 규칙 템플릿을 입력으로 지식 그래프로부터 새로운 지식을 추론할 수 있는 규칙을 자동으로 유도하는 end-to-end leanring을 제공합니다.  
해당 코드에 대한 documentation은 [`Neuro-Symbolic/NTP/NTP_docu_1013.pdf`](https://github.com/ShinWon-Chul/Neuro-Symbolic/blob/main/NTP/NTP_docu_1013.pdf)를 참조 하십시오.  
해당 코드에 대한 직관적인 파악은 [`Neuro-Symbolic/papers/CSCI_NTP.pdf`](https://github.com/ShinWon-Chul/Neuro-Symbolic/blob/main/papers/CSCI_NTP.pdf)를 참조 하십시오.

## 데이터 형식
NTP의 데이터는 `.txt` 기본적으로 트리플(subject, relation, object)형식을 따릅니다.

```shell
NTP/data/example_7.txt
BART	nationality	USA
BART	placeOfBirth	NEWYORK
NEWYORK	locatedIn	USA
BART	hasFather	HOMER
HOMER	nationality	USA
HOMER	placeOfBirth	NEWYORK
BART	bornIn	USA
```

- `*.txt` 파일은 *fact*를 나타냅니다. (example of a fact: `BART hasFather HOMER`)

- `*.nlt` 파일은 *rule templates*을 나타냅니다. (example of a rule template: `#1(X,Y) :- #2(X,Z), #3(Z,Y)`)

```shell
NTP/data/example_7.nlt
2	#1(X, Y) :- #2(X, Z),#3(Z, Y).
2	#1(X, Y) :- #2(X, Y).
```

## Running

NTP를 실행하기 위한 기본 파일은 `ntp/Neural Theorem Prover_v2.0.ipynb` 입니다.