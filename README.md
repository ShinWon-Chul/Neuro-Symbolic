# Knowledge Inference and Knowledge Completion Methods using Neuro-Symbolic Inductive Rules
해당 레파지토리는 [뉴로 심볼릭 유도 규칙을 활용한 지식 추론 및 지식 완성 방법](/papers/%EB%89%B4%EB%A1%9C%20%EC%8B%AC%EB%B3%BC%EB%A6%AD%20%EA%B8%B0%EB%B0%98%20%EA%B7%9C%EC%B9%99%20%EC%9C%A0%EB%8F%84%20%EB%B0%8F%20%EC%B6%94%EB%A1%A0%20%EC%97%94%EC%A7%84%EC%9D%84%20%ED%99%9C%EC%9A%A9%ED%95%9C%20%EC%A7%80%EC%8B%9D%20%EC%99%84%EC%84%B1%20%EC%8B%9C%EC%8A%A4%ED%85%9C.pdf)를 구현한 것입니다.  
해당 코드는 지식 그래프와 규칙 템플릿을 입력으로 지식 그래프로부터 새로운 지식을 추론할 수 있는 규칙을 자동으로 유도하는 end-to-end leanring을 제공하며 다음과 관계에 해당하는 추론 규칙을 유도합니다.  

- transitivity : `X (rel) Z and Z (rel) Y then X (rel) Y`
- inverse : `X (rel) Y then Y (rel) X`
- equality : `X (rel) Y then X (rel) Y`  

해당 코드에 대한 직관적인 파악은 [`papers/CSCI_NTP.pdf`](/papers/CSCI_NTP.pdf)를 참조 하십시오.

## Input Data Format
입력 데이터의 `*.txt` 파일은 지식 그래프로 기본적으로 트리플(subject, relation, object)형식을 따릅니다.
- `*.txt` 파일의 각 line은 **fact**를 나타냅니다. 
	- fact: `BART hasFather HOMER`  

<br/>

입력 데이터의 `*.nlt` 파일은 규칙 템플릿이 저장되어 있습니다.  
- `*.nlt` 파일의 각 line은 **rule templates**을 나타냅니다. 
	- rule template: `2	 #1(X,Y) :- #2(X,Z), #3(Z,Y)`
- rule template은 augment number, rule schema가 `tab`으로 분리되어있는 형태입니다.
	- augment number : `2`
	- rule schema : `#1(X, Y) :- #2(X, Z),#3(Z, Y).`  
- augment number는 입력 지식 그래프로부터 해당 rule schema형태의 rule instance생성 개수를 의미합니다.  
- rule schema는 `:-`를 기준으로 좌변은 conclusion, 우변은 conclusion을 추론하기 위한 condition으로 구성됩니다.  
	- 좌변 : `#1(X, Y)`
	- 우변 : `#2(X, Z),#3(Z, Y)`

<br/>

아래의 `.txt` 파일과 `.nlt` 파일로부터 유도된 규칙은 아래의 **Output Example**을 참조 하십시오  
[`NTP/data/example_8.txt`](/NTP/data/example_8.txt)
```shell
BART	nationality	USA
BART	birthPlace	NEWYORK
NEWYORK	locatedIn	USA
BART	hasFather	HOMER
BART	hasGrandfather	ABE
HOMER	hasParent	ABE
LISA	sibling		BART
BART	sibling		LISA
``` 

[`NTP/data/example_8.nlt`](/NTP/data/example_8.nlt)
```shell
2	#1(X, Y) :- #2(X, Z),#3(Z, Y).
2	#1(X, Y) :- #2(Y, X).
```

## Output Example
[`/NTP/out/example_8/example_8_rule.tsv`](/NTP/out/example_8/example_8_rule.tsv)
```shell
(('p0_0', 'X', 'Y'), ('p1_0', 'X', 'Z'), ('p2_0', 'Z', 'Y'))
0.952875	nationality(X,Y) :- birthPlace(X,Z), locatedIn(Z,Y)
0.892625	hasGrandfather(X,Y) :- hasFather(X,Z), hasParent(Z,Y)

(('p0_1', 'X', 'Y'), ('p1_1', 'Y', 'X'))
0.957433	sibling(X,Y) :- sibling(Y,X)
0.021941	sibling(X,Y) :- sibling(Y,X)
```

## Running

NTP를 실행하기 위한 기본 파일은 [`NTP/Neural Theorem Prover_v2.1.ipynb`](/NTP/Neural%20Theorem%20Prover_v2.1.ipynb) 입니다.