# 하루코딩 커리큘럼 원본. 실행: python3 content/course.py  ->  www/course.js
import json, os

def mc(q, o, e='', code=None):
    d = {'k': 'mc', 'q': q, 'o': o, 'e': e}
    if code: d['code'] = code
    return d
def out(code, o, e='', q=None):
    d = {'k': 'out', 'code': code, 'o': o, 'e': e}
    if q: d['q'] = q
    return d
def fill(q, code, o, e=''):
    return {'k': 'fill', 'q': q, 'code': code, 'o': o, 'e': e}
def order(q, lines, e=''):
    return {'k': 'order', 'q': q, 'lines': lines, 'e': e}
def bug(code, a, e='', q=None):
    d = {'k': 'bug', 'code': code, 'a': a, 'e': e}
    if q: d['q'] = q
    return d
def task(q, sol, e='', **kw):
    d = {'k': 'code', 'q': q, 'sol': sol, 'e': e}
    d.update(kw)
    return d
def card(h, p, code=None, **kw):
    d = {'h': h, 'p': p}
    if code: d['code'] = code
    d.update(kw)
    return d

# ------------------------------------------------------------------ Python
PY = [
 dict(id='py1', t='화면에 출력하기', ic='print', d='print로 글자를 보여 주는 첫 프로그램', cards=[
  card('프로그램은 명령의 목록', '컴퓨터는 코드를 <b>위에서 아래로 한 줄씩</b> 실행해요. 첫 명령은 화면에 글자를 보여 주는 <code>print()</code>예요.', 'print("안녕하세요")\nprint("파이썬 시작!")'),
  card('문자열은 따옴표로', '글자 묶음을 <b>문자열</b>이라고 해요. 큰따옴표 <code>"..."</code>나 작은따옴표 <code>\'...\'</code>로 감싸요. 따옴표가 없으면 파이썬은 그걸 변수 이름으로 생각해요.', "print('작은따옴표도 돼요')\nprint(\"큰따옴표도 돼요\")"),
  card('여러 값과 주석', '쉼표로 여러 값을 넘기면 사이에 공백을 넣어 출력해요. 숫자는 따옴표 없이 써요. <code>#</code> 뒤는 <b>주석</b>이라 실행되지 않아요. 나중에 볼 메모를 남길 때 써요.', '# 이 줄은 실행되지 않아요\nprint("나이:", 20)\nprint(1, 2, 3)'),
 ], q=[
  mc('화면에 글자를 출력하는 명령은?', ['print()', 'show()', 'echo', 'write'], '파이썬에서 출력은 print()예요.'),
  out('print("Hello")', ['Hello', '"Hello"', 'print("Hello")', '에러'], '따옴표는 문자열을 감싸는 표시라 화면에는 나오지 않아요.'),
  out('print("나이:", 20)', ['나이: 20', '나이:20', '"나이:", 20', '나이: "20"'], '쉼표로 나눈 값들은 사이에 공백 한 칸을 넣어 출력돼요.'),
  fill('"반가워요"를 출력하세요', 'print(▢)', ['"반가워요"', '반가워요', '(반가워요)', '<반가워요>'], '문자열은 따옴표로 감싸야 해요.'),
  bug('print("하나")\nprint(둘)\nprint("셋")', 1, '둘에 따옴표가 없어서 파이썬이 \'둘\'이라는 변수를 찾다가 NameError가 나요.'),
  mc('파이썬의 주석은?', ['# 메모', '// 메모', '<!-- 메모 -->', '-- 메모'], '파이썬 주석은 #으로 시작해요. //는 JavaScript, <!-- -->는 HTML 주석이에요.'),
  out('print(1, 2, 3)', ['1 2 3', '123', '1,2,3', '(1, 2, 3)'], ''),
  order('"하나", "둘", "셋" 순서로 출력되게 줄을 놓으세요', ['print("하나")', 'print("둘")', 'print("셋")'], '코드는 위에서 아래로 실행돼요.'),
  task('print로 Hello, World! 를 출력해 보세요', 'print("Hello, World!")', '프로그래밍을 배울 때 전통적으로 처음 출력하는 문장이에요.', expect='Hello, World!'),
  task('두 줄로 1일차 와 파이썬 공부 중 을 출력하세요', 'print("1일차")\nprint("파이썬 공부 중")', 'print를 두 번 쓰면 두 줄이 돼요.', expect='1일차\n파이썬 공부 중'),
 ]),
 dict(id='py2', t='변수', ic='x =', d='값에 이름을 붙여 저장하기', cards=[
  card('변수는 이름표 붙은 상자', '<code>이름 = 값</code>으로 값을 저장해요. 여기서 <code>=</code>는 "같다"가 아니라 <b>"오른쪽 값을 왼쪽 이름에 넣어라"</b>는 뜻이에요.', 'name = "민수"\nage = 25\nprint(name, age)'),
  card('값 바꾸기', '같은 이름에 다시 넣으면 이전 값은 사라지고 새 값만 남아요.', 'score = 10\nscore = 20\nprint(score)'),
  card('이름 짓는 규칙', '글자·숫자·밑줄(_)로 만들고, 숫자로 시작할 수 없어요. 파이썬은 <code>나이 = 20</code>처럼 한글 이름도 허용하지만, 다른 사람과 함께 쓰는 코드에서는 <b>영문 이름을 쓰는 게 관례</b>예요. 띄어쓰기 대신 <code>my_name</code>처럼 밑줄을 써요. 대문자와 소문자는 다른 글자로 취급해요.', 'my_name = "지영"\nprint(my_name)'),
 ], q=[
  out('x = 5\nprint(x)', ['5', 'x', '"5"', '에러']),
  out('x = 5\nx = 8\nprint(x)', ['8', '5', '13', '5 8'], '마지막에 넣은 값 8만 남아요.'),
  out('a = "사과"\nprint("a")', ['a', '사과', '"사과"', '에러'], '따옴표로 감싼 "a"는 변수가 아니라 글자 a 그 자체예요.'),
  mc('변수 이름으로 쓸 수 없는 것은?', ['2nd_place', 'place2', '_place', 'placeTwo'], '숫자로 시작하는 이름은 쓸 수 없어요.'),
  fill('변수 city에 "서울"을 저장하세요', 'city ▢ "서울"', ['=', '==', ':', '->'], '저장(대입)은 = 한 개예요. ==는 비교할 때 써요.'),
  out('a = 3\nb = a\na = 10\nprint(b)', ['3', '10', 'a', '13'], 'b = a 를 실행한 순간 b에는 3이 들어갔고, 나중에 a를 바꿔도 b는 그대로예요.'),
  bug('my age = 20\nprint(my age)', 0, '변수 이름에 띄어쓰기를 쓸 수 없어요. my_age처럼 밑줄을 써요.'),
  mc('Name과 name은?', ['서로 다른 변수', '같은 변수', '에러', 'Name만 쓸 수 있다'], '파이썬은 대문자와 소문자를 구분해요.'),
  task('변수 food에 "피자"를 저장하고 출력하세요', 'food = "피자"\nprint(food)', '', expect='피자', need=[r'food\s*=']),
  task('변수 a에 1, b에 2를 넣고 print(a, b)로 출력하세요', 'a = 1\nb = 2\nprint(a, b)', '', expect='1 2', need=[r'a\s*=', r'b\s*=']),
 ]),
 dict(id='py3', t='숫자와 계산', ic='+ -', d='사칙연산, 몫과 나머지, 문자열 계산', cards=[
  card('사칙연산', '<code>+ - * /</code>를 써요. 곱하기는 <code>*</code>, 나누기는 <code>/</code>예요. <code>/</code>의 결과는 항상 소수(float)로 나와요.', 'print(3 + 4)\nprint(10 - 3)\nprint(6 * 7)\nprint(7 / 2)'),
  card('몫·나머지·거듭제곱', '<code>//</code>는 몫, <code>%</code>는 나머지, <code>**</code>는 거듭제곱이에요. 나머지는 짝수·홀수를 가릴 때 자주 써요.', 'print(7 // 2)\nprint(7 % 2)\nprint(2 ** 10)'),
  card('문자열과 숫자는 달라요', '<code>"3"</code>은 글자, <code>3</code>은 숫자예요. 문자열끼리 <code>+</code>하면 이어 붙이고, 문자열 <code>*</code> 숫자는 반복해요. 문자열과 숫자를 <code>+</code>하면 에러라서 <code>str()</code>로 바꿔요.', 'print("3" + "4")\nprint("하" * 3)\nprint("나이: " + str(20))'),
 ], q=[
  out('print(2 + 3 * 4)', ['14', '20', '24', '2 + 3 * 4'], '수학처럼 곱셈이 덧셈보다 먼저예요.'),
  out('print(10 / 4)', ['2.5', '2', '2.0', '3']),
  out('print(10 // 4)', ['2', '2.5', '3', '0'], '//는 소수점 아래를 버린 몫이에요.'),
  out('print(10 % 4)', ['2', '2.5', '0', '4'], '10을 4로 나누면 몫 2, 나머지 2예요.'),
  out('print("5" + "5")', ['55', '10', '"55"', '에러'], '문자열끼리 더하면 이어 붙여요.'),
  out('print("ab" * 3)', ['ababab', 'ab3', 'ab ab ab', '에러']),
  mc('print("나이: " + 20) 을 실행하면?', ['TypeError 에러', '나이: 20', '나이: "20"', '나이:20'], '문자열과 숫자는 +로 바로 붙일 수 없어요. str(20)으로 바꾸거나 print("나이:", 20)처럼 쉼표를 써요.'),
  fill('2의 3제곱(8)을 출력하세요', 'print(2 ▢ 3)', ['**', '^', '*', '//'], '파이썬에서 ^는 거듭제곱이 아니라 다른 연산이에요.'),
  task('price와 count를 곱한 총액을 출력하세요', 'price = 1200\ncount = 3\nprint(price * count)', '', start='price = 1200\ncount = 3\n', expect='3600'),
  task('100을 7로 나눈 몫과 나머지를 print(몫, 나머지)로 출력하세요', 'print(100 // 7, 100 % 7)', '', expect='14 2', need=['//', '%']),
 ]),
 dict(id='py4', t='입력 받기', ic='input', d='사용자 입력과 f-문자열', cards=[
  card('input()으로 물어보기', '<code>input("질문")</code>은 질문을 보여 주고, 사용자가 입력한 글자를 돌려줘요. 이 앱에서는 <b>입력값 칸</b>에 미리 적어 둔 값이 차례로 들어가요.', 'name = input("이름이 뭐예요? ")\nprint("반가워요,", name)', stdin=['민수']),
  card('입력은 항상 문자열', '숫자를 입력해도 <code>"20"</code> 같은 문자열이에요. 계산하려면 <code>int()</code>로 정수, <code>float()</code>로 소수로 바꿔요.', 'age = int(input("나이: "))\nprint("내년엔", age + 1, "살")', stdin=['20']),
  card('f-문자열', '문자열 앞에 <code>f</code>를 붙이고 <code>{변수}</code>를 쓰면 그 자리에 값이 들어가요. 실무에서 가장 많이 쓰는 방법이에요.', 'name = "지영"\nage = 30\nprint(f"{name}님은 {age}살이에요")'),
 ], q=[
  mc('input()이 돌려주는 값의 종류는?', ['항상 문자열', '항상 숫자', '입력에 따라 다름', 'True 또는 False'], '숫자를 입력해도 문자열이에요.'),
  out('x = "7"\nprint(x * 2)', ['77', '14', '에러', '7 7'], '"7"은 문자열이라 * 2는 반복이에요.'),
  out('x = int("7")\nprint(x * 2)', ['14', '77', '에러', '7']),
  fill('입력받은 값을 정수로 바꾸세요', 'n = ▢(input())', ['int', 'str', 'num', 'text'], 'int()는 정수, float()는 소수, str()은 문자열로 바꿔요.'),
  out('name = "철수"\nprint(f"안녕 {name}")', ['안녕 철수', '안녕 {name}', 'f안녕 철수', '안녕 name']),
  out('print(f"{3 + 4}")', ['7', '3 + 4', '{3 + 4}', '34'], '{ } 안에는 계산식도 쓸 수 있어요.'),
  bug('age = input("나이: ")\nprint(age + 1)', 0, 'age는 문자열이라 1을 더할 수 없어요. age = int(input("나이: "))로 바꿔야 해요.', q='어느 줄을 고쳐야 할까요?'),
  mc('print(f"합: {a+b}")에서 f를 빼면?', ['합: {a+b} 가 그대로 출력된다', '계산 결과가 출력된다', '에러가 난다', '아무것도 안 나온다'], 'f가 있어야 { } 안을 계산해요.'),
  task('이름을 입력받아 안녕, 이름! 형태로 출력하세요', 'name = input()\nprint(f"안녕, {name}!")', '', stdin=['지수'], contains=['안녕, 지수!'], need=['input']),
  task('숫자 두 개를 차례로 입력받아 합을 출력하세요', 'a = int(input())\nb = int(input())\nprint(a + b)', '', stdin=['3', '5'], contains=['8'], need=['input', 'int']),
 ]),
 dict(id='py5', t='조건문 if', ic='if', d='조건에 따라 다르게 실행하기', cards=[
  card('비교하면 True / False', '<code>==</code> 같다, <code>!=</code> 다르다, <code>&gt; &lt; &gt;= &lt;=</code> 크기 비교. 결과는 참(<code>True</code>) 또는 거짓(<code>False</code>)이에요.', 'print(3 > 2)\nprint(3 == 4)\nprint("a" != "b")'),
  card('if와 들여쓰기', '<code>if 조건:</code> 다음 줄을 <b>4칸 들여 쓰면</b> 조건이 참일 때만 실행돼요. 콜론(:)과 들여쓰기가 파이썬 문법의 핵심이에요.', 'score = 85\nif score >= 80:\n    print("합격!")\nprint("끝")'),
  card('elif와 else', '<code>elif</code>는 "아니면 이 조건", <code>else</code>는 "모두 아니면". 위에서부터 처음 참인 곳 <b>하나만</b> 실행돼요.', 'score = 72\nif score >= 90:\n    print("A")\nelif score >= 70:\n    print("B")\nelse:\n    print("C")'),
  card('and, or, not', '<code>and</code> 둘 다 참, <code>or</code> 하나라도 참, <code>not</code>은 반대예요.', 'age = 20\nprint(age >= 19 and age < 30)\nprint(not True)'),
 ], q=[
  out('print(5 == 5)', ['True', 'False', '5', '에러']),
  out('x = 3\nif x > 5:\n    print("크다")\nprint("끝")', ['끝', '크다\n끝', '크다', '아무것도 안 나옴'], '조건이 거짓이라 들여 쓴 줄은 건너뛰고, 들여 쓰지 않은 print("끝")만 실행돼요.'),
  out('x = 10\nif x > 5:\n    print("크다")\nelse:\n    print("작다")', ['크다', '작다', '크다\n작다', '에러']),
  out('n = 0\nif n > 0:\n    print("양수")\nelif n == 0:\n    print("영")\nelse:\n    print("음수")', ['영', '양수', '음수', '영\n음수']),
  mc('같은지 비교하는 연산자는?', ['==', '=', '===', '!='], '=는 저장, ==는 비교예요. ===는 JavaScript에서 써요.'),
  bug('age = 20\nif age >= 19\n    print("성인")', 1, 'if 줄 끝에 콜론(:)이 빠졌어요.'),
  bug('x = 5\nif x > 3:\nprint("크다")', 2, 'if 아래 줄은 4칸 들여 써야 해요. 안 그러면 IndentationError가 나요.'),
  out('print(3 > 1 and 2 > 5)', ['False', 'True', '3', '에러'], '뒤쪽 2 > 5가 거짓이라 and 결과도 거짓이에요.'),
  fill('짝수일 때 "짝수"를 출력하세요', 'n = 4\nif n % 2 ▢ 0:\n    print("짝수")', ['==', '=', '!=', '>'], '2로 나눈 나머지가 0이면 짝수예요.'),
  order('x가 음수면 "음수", 아니면 "0 이상"을 출력하도록', ['x = -3', 'if x < 0:', '    print("음수")', 'else:', '    print("0 이상")']),
  task('temp가 30 이상이면 더워요, 아니면 괜찮아요를 출력하세요', 'temp = 32\nif temp >= 30:\n    print("더워요")\nelse:\n    print("괜찮아요")', '', start='temp = 32\n', expect='더워요', need=['if', 'else']),
  task('score가 90 이상이면 A, 80 이상이면 B, 그 외는 C를 출력하세요', 'score = 85\nif score >= 90:\n    print("A")\nelif score >= 80:\n    print("B")\nelse:\n    print("C")', '', start='score = 85\n', expect='B', need=['elif']),
 ]),
 dict(id='py6', t='반복문', ic='for', d='for와 while로 여러 번 실행하기', cards=[
  card('for와 range', '<code>for i in range(5):</code>는 i를 0, 1, 2, 3, 4로 바꿔 가며 5번 반복해요. <code>range(시작, 끝)</code>은 <b>끝 바로 앞까지</b>예요.', 'for i in range(3):\n    print("반복", i)\nfor n in range(1, 4):\n    print(n)'),
  card('누적하기', '반복 전에 변수를 0으로 만들고, 반복하면서 더해 가는 방법을 정말 자주 써요.', 'total = 0\nfor n in range(1, 11):\n    total = total + n\nprint(total)'),
  card('while과 break', '<code>while 조건:</code>은 조건이 참인 동안 계속 반복해요. 조건이 영원히 참이면 끝나지 않으니 조심! <code>break</code>는 반복을 즉시 멈춰요.', 'count = 3\nwhile count > 0:\n    print(count)\n    count = count - 1\nprint("발사!")'),
 ], q=[
  out('for i in range(3):\n    print(i)', ['0\n1\n2', '1\n2\n3', '0\n1\n2\n3', '3'], 'range(3)은 0, 1, 2예요.'),
  out('for i in range(2, 5):\n    print(i)', ['2\n3\n4', '2\n3\n4\n5', '3\n4', '2 3 4'], '끝 숫자 5는 포함하지 않아요.'),
  mc('range(5)가 만드는 숫자는 몇 개?', ['5개', '4개', '6개', '무한'], '0부터 4까지 5개예요.'),
  out('t = 0\nfor n in range(1, 5):\n    t = t + n\nprint(t)', ['10', '15', '4', '0'], '1 + 2 + 3 + 4 = 10'),
  out('for c in "abc":\n    print(c)', ['a\nb\nc', 'abc', 'a b c', '에러'], 'for는 문자열의 글자도 하나씩 꺼내 줘요.'),
  out('i = 0\nwhile i < 3:\n    i = i + 1\nprint(i)', ['3', '2', '0', '무한 반복']),
  mc('이 코드의 문제는?', ['n이 줄지 않아 끝나지 않는다', '5가 한 번만 출력된다', '문법 에러', '아무것도 출력되지 않는다'], 'n을 줄이는 줄(n = n - 1)이 없어서 조건이 영원히 참이에요.', code='n = 5\nwhile n > 0:\n    print(n)'),
  out('for i in range(10):\n    if i == 3:\n        break\n    print(i)', ['0\n1\n2', '0\n1\n2\n3', '3', '0부터 9까지 전부'], 'i가 3이 되는 순간 break로 멈춰요.'),
  fill('1부터 5까지 출력하세요', 'for i in range(1, ▢):\n    print(i)', ['6', '5', '4', '1'], '끝 숫자는 포함하지 않아서 6을 써야 5까지 나와요.'),
  task('for와 range로 안녕을 3번 출력하세요', 'for i in range(3):\n    print("안녕")', '', expect='안녕\n안녕\n안녕', need=['for']),
  task('1부터 100까지의 합을 for로 구해 출력하세요', 'total = 0\nfor n in range(1, 101):\n    total = total + n\nprint(total)', '', expect='5050', need=['for']),
 ]),
 dict(id='py7', t='리스트', ic='[ ]', d='여러 값을 한 번에 다루기', cards=[
  card('여러 값을 한 줄에', '<code>[ ]</code> 안에 쉼표로 값을 넣으면 리스트예요. 번호(인덱스)는 <b>0부터</b> 시작하고, <code>-1</code>은 맨 뒤예요. <code>len()</code>은 개수.', 'fruits = ["사과", "바나나", "포도"]\nprint(fruits[0])\nprint(fruits[-1])\nprint(len(fruits))'),
  card('추가·수정', '<code>append()</code>로 맨 뒤에 추가, <code>리스트[번호] = 값</code>으로 수정해요.', 'nums = [1, 2]\nnums.append(3)\nnums[0] = 10\nprint(nums)'),
  card('리스트와 for', '<code>for 변수 in 리스트:</code>로 값을 하나씩 꺼낼 수 있어요. <code>sum()</code>, <code>max()</code>, <code>min()</code>도 편리해요.', 'scores = [80, 95, 70]\nfor s in scores:\n    print(s)\nprint(sum(scores), max(scores))'),
 ], q=[
  out('a = [10, 20, 30]\nprint(a[1])', ['20', '10', '30', '에러'], '번호는 0부터 세요.'),
  out('a = [10, 20, 30]\nprint(a[-1])', ['30', '10', '에러', '-1']),
  out('print(len([1, 2, 3, 4]))', ['4', '3', '10', '5']),
  out('a = [1, 2]\na.append(5)\nprint(a)', ['[1, 2, 5]', '[5, 1, 2]', '[1, 2]', '[1, 2, [5]]']),
  mc('a = [1, 2, 3] 에서 a[3]을 쓰면?', ['IndexError 에러', '3', '0', 'None'], '번호는 0, 1, 2까지라 3은 범위 밖이에요.'),
  out('a = ["x", "y"]\na[0] = "z"\nprint(a)', ["['z', 'y']", "['x', 'z']", "['z', 'x', 'y']", '에러']),
  fill('리스트에 "포도"를 추가하세요', 'fruits.▢("포도")', ['append', 'add', 'push', 'insert'], 'push는 JavaScript, add는 집합(set)에서 써요.'),
  out('print(sum([1, 2, 3]))', ['6', '123', '[1, 2, 3]', '3']),
  order('리스트의 값을 하나씩 출력하세요', ['names = ["가", "나"]', 'for n in names:', '    print(n)']),
  task('nums의 가장 큰 값을 출력하세요', 'nums = [3, 8, 1]\nprint(max(nums))', '', start='nums = [3, 8, 1]\n', expect='8'),
  task('빈 리스트 a를 만들고 1, 2, 3을 append로 넣은 뒤 출력하세요', 'a = []\na.append(1)\na.append(2)\na.append(3)\nprint(a)', '', expect='[1, 2, 3]', need=['append']),
 ]),
 dict(id='py8', t='함수', ic='def', d='코드를 묶어 이름 붙이기', cards=[
  card('함수는 이름 붙인 코드 묶음', '<code>def 이름():</code>으로 만들고 <code>이름()</code>으로 불러서 실행해요. 만들기만 하고 부르지 않으면 실행되지 않아요.', 'def hello():\n    print("안녕!")\n\nhello()\nhello()'),
  card('매개변수', '괄호 안에 값을 받을 이름을 정하면, 부를 때 넘긴 값이 들어가요.', 'def greet(name):\n    print(f"{name}님 안녕하세요")\n\ngreet("민수")\ngreet("지영")'),
  card('return으로 값 돌려주기', '<code>return</code>은 결과 값을 돌려주고 함수를 끝내요. 돌려받은 값은 변수에 저장하거나 바로 출력할 수 있어요.', 'def add(a, b):\n    return a + b\n\nresult = add(3, 4)\nprint(result)'),
 ], q=[
  mc('함수를 만들 때 쓰는 키워드는?', ['def', 'function', 'func', 'fn'], 'function은 JavaScript에서 써요.'),
  out('def f():\n    print("A")\nprint("B")', ['B', 'A\nB', 'A', 'B\nA'], '함수는 만들기만 하고 부르지 않으면 실행되지 않아요.'),
  out('def double(x):\n    return x * 2\nprint(double(5))', ['10', '5', 'x * 2', 'None']),
  out('def f(a, b):\n    return a - b\nprint(f(2, 7))', ['-5', '5', '27', '에러'], 'a에 2, b에 7이 들어가요.'),
  out('def f():\n    print("hi")\nresult = f()\nprint(result)', ['hi\nNone', 'hi', 'None', 'hi\nhi'], 'return이 없는 함수는 None을 돌려줘요.'),
  fill('두 수를 곱해 돌려주는 함수', 'def mul(a, b):\n    ▢ a * b', ['return', 'print', 'give', 'def']),
  bug('def say(msg)\n    print(msg)\nsay("hi")', 0, 'def 줄 끝에 콜론(:)이 필요해요.'),
  mc('함수 안에서 return 아래에 있는 코드는?', ['실행되지 않는다', '두 번 실행된다', '에러가 난다', '먼저 실행된다'], 'return을 만나면 함수가 바로 끝나요.'),
  order('함수를 만들고 부르세요', ['def cheer(name):', '    print(name + " 화이팅!")', 'cheer("민수")']),
  task('숫자를 받아 제곱을 돌려주는 함수 square를 만들고 print(square(6))을 실행하세요', 'def square(n):\n    return n * n\n\nprint(square(6))', '', expect='36', need=[r'def\s+square', 'return'], test='print(square(-3), square(0), square(12))', testOut='9 0 144'),
  task('이름을 받아 이름님 환영해요를 출력하는 함수 welcome을 만들고 welcome("하나")를 실행하세요', 'def welcome(name):\n    print(f"{name}님 환영해요")\n\nwelcome("하나")', '', expect='하나님 환영해요', need=[r'def\s+welcome'], test='welcome("둘")', testOut='둘님 환영해요'),
 ]),
]

# ------------------------------------------------------------------ HTML / CSS
HT = [
 dict(id='ht1', t='HTML과 태그', ic='<h1>', d='웹페이지의 뼈대 만들기', cards=[
  card('HTML은 웹페이지의 뼈대', '내용을 <b>태그</b>로 감싸서 "이건 제목, 이건 문단"이라고 알려 줘요. <code>&lt;h1&gt;</code> 같은 여는 태그와 <code>&lt;/h1&gt;</code> 같은 닫는 태그 사이에 내용을 넣어요.', '<h1>나의 첫 웹페이지</h1>\n<p>안녕하세요! 반가워요.</p>'),
  card('제목은 h1~h6', '<code>h1</code>이 가장 크고 중요한 제목, <code>h6</code>이 가장 작아요. 문단은 <code>p</code>, 줄바꿈은 <code>&lt;br&gt;</code>이에요. br은 닫는 태그가 없어요.', '<h1>큰 제목</h1>\n<h2>중간 제목</h2>\n<h3>작은 제목</h3>\n<p>첫 줄<br>둘째 줄</p>'),
  card('글자 강조', '<code>&lt;strong&gt;</code>은 중요(굵게), <code>&lt;em&gt;</code>은 강조(기울임)예요.', '<p>오늘은 <strong>꼭</strong> <em>복습</em>하기</p>'),
 ], q=[
  mc('가장 큰 제목 태그는?', ['<h1>', '<h6>', '<head>', '<title>']),
  mc('닫는 태그의 모양은?', ['</p>', '<p/>', '<\\p>', '<p>'], '닫는 태그는 이름 앞에 /를 붙여요.'),
  mc('문단을 만드는 태그는?', ['<p>', '<para>', '<text>', '<pg>'], 'p는 paragraph(문단)의 첫 글자예요.'),
  out('<p>안녕<br>하세요</p>', ['안녕\n하세요 (두 줄)', '안녕하세요 (한 줄)', '안녕<br>하세요', '하세요\n안녕'], 'br은 줄을 바꿔요.', q='화면에 어떻게 보일까요?'),
  bug('<h1>제목</h1>\n<p>문단입니다<p>', 1, '닫는 태그는 </p>처럼 /가 있어야 해요.'),
  fill('"중요"를 굵게(중요 표시) 만드세요', '<p>정말 ▢중요</strong>해요</p>', ['<strong>', '<strong/>', '</strong>', '<bold>']),
  mc('<br> 태그의 특징은?', ['닫는 태그가 없다', '반드시 </br>로 닫는다', '제목을 만든다', '글자를 굵게 만든다']),
  order('큰 제목, 작은 제목, 문단 순서로 놓으세요', ['<h1>여행 일기</h1>', '<h2>1일차</h2>', '<p>오늘은 바다에 갔다.</p>']),
  task('h1 태그로 안녕 HTML 이라는 제목을 만드세요', '<h1>안녕 HTML</h1>', '', check='(doc.querySelector("h1")||{}).textContent.trim()==="안녕 HTML"'),
  task('제목(h1) 하나와 문단(p) 두 개를 만드세요 (내용은 자유)', '<h1>제목</h1>\n<p>첫 문단</p>\n<p>둘째 문단</p>', '', check='doc.querySelectorAll("h1").length>=1&&doc.querySelectorAll("p").length>=2'),
 ]),
 dict(id='ht2', t='문서 구조', ic='</>', d='head와 body, 완성된 HTML 문서', cards=[
  card('HTML 문서의 기본 틀', '완성된 문서는 <code>&lt;!DOCTYPE html&gt;</code>로 시작하고, <code>&lt;html&gt;</code> 안에 <code>&lt;head&gt;</code>(정보)와 <code>&lt;body&gt;</code>(보이는 내용)가 들어가요.', '<!DOCTYPE html>\n<html>\n<head>\n  <meta charset="utf-8">\n  <title>탭에 보이는 제목</title>\n</head>\n<body>\n  <h1>본문 내용</h1>\n</body>\n</html>'),
  card('head와 body', 'head에는 탭 제목(<code>title</code>), 한글이 깨지지 않게 하는 <code>&lt;meta charset="utf-8"&gt;</code> 같은 정보를 넣어요. 화면에 보이는 건 모두 body에 넣어요.', '<head>\n  <meta charset="utf-8">\n  <title>내 블로그</title>\n</head>\n<body>\n  <p>보이는 내용은 여기!</p>\n</body>'),
  card('들여쓰기와 주석', '안쪽 태그를 들여 쓰면 구조가 한눈에 보여요. <code>&lt;!-- --&gt;</code>는 주석이라 화면에 나오지 않아요.', '<body>\n  <!-- 메뉴 영역 -->\n  <h1>내 블로그</h1>\n</body>'),
 ], q=[
  mc('화면에 보이는 내용은 어디에 넣나요?', ['<body>', '<head>', '<title>', '<meta>']),
  mc('브라우저 탭에 표시되는 제목 태그는?', ['<title>', '<h1>', '<head>', '<tab>']),
  mc('HTML 문서 맨 첫 줄에 쓰는 것은?', ['<!DOCTYPE html>', '<html>', '<start>', '<!-- html -->']),
  mc('HTML의 주석은?', ['<!-- 메모 -->', '# 메모', '// 메모', '/* 메모 */'], '/* */는 CSS 주석이에요.'),
  order('HTML 기본 틀을 순서대로 놓으세요', ['<!DOCTYPE html>', '<html>', '<head><title>홈</title></head>', '<body><h1>환영</h1></body>', '</html>']),
  bug('<html>\n<head>\n  <h1>제목</h1>\n</head>\n<body></body>\n</html>', 2, 'h1처럼 화면에 보일 내용은 head가 아니라 body에 넣어야 해요.'),
  mc('한글이 깨지지 않게 head에 넣는 것은?', ['<meta charset="utf-8">', '<lang>한국어</lang>', '<font>', '<korean>']),
  fill('본문 영역을 여세요', '<html>\n  ▢\n    <p>내용</p>\n  </body>\n</html>', ['<body>', '<head>', '<main/>', '</body>']),
  task('body 안에 h1으로 My Page 를 넣으세요', '<!DOCTYPE html>\n<html>\n<head>\n  <title>연습</title>\n</head>\n<body>\n  <h1>My Page</h1>\n</body>\n</html>', '', start='<!DOCTYPE html>\n<html>\n<head>\n  <title>연습</title>\n</head>\n<body>\n  \n</body>\n</html>', check='(doc.querySelector("body h1")||{}).textContent==="My Page"'),
  task('주석과 함께 본문 이라고 쓴 p 태그를 넣으세요', '<!-- 시작 -->\n<p>본문</p>', '', check='(()=>{const w=doc.createTreeWalker(doc,128);return !!w.nextNode()})()&&[...doc.querySelectorAll("p")].some(p=>p.textContent.trim()==="본문")'),
 ]),
 dict(id='ht3', t='링크와 이미지', ic='<a>', d='다른 페이지로 이동하고 그림 넣기', cards=[
  card('링크 a', '<code>&lt;a href="주소"&gt;글자&lt;/a&gt;</code>를 누르면 그 주소로 이동해요. <code>href</code>처럼 태그에 붙는 설정값을 <b>속성</b>이라고 해요.', '<a href="https://www.naver.com">네이버로 가기</a>'),
  card('새 탭에서 열기', '<code>target="_blank"</code> 속성을 더하면 새 탭에서 열려요.', '<a href="https://www.google.com" target="_blank">구글 (새 탭)</a>'),
  card('이미지 img', '<code>&lt;img src="주소" alt="설명"&gt;</code>. 닫는 태그가 없어요. <code>alt</code>는 그림이 안 보일 때나 화면 낭독기가 읽어 주는 설명이에요. <code>width</code>로 크기를 정해요.', '<img src="https://picsum.photos/240/140" alt="풍경 사진" width="240">'),
 ], q=[
  mc('링크를 만드는 태그는?', ['<a>', '<link>', '<href>', '<url>'], '<link>는 head에서 CSS 파일 등을 연결할 때 써요.'),
  mc('링크 주소를 넣는 속성은?', ['href', 'src', 'link', 'to']),
  mc('이미지 주소를 넣는 속성은?', ['src', 'href', 'img', 'url']),
  mc('img의 alt 속성 역할은?', ['그림 설명 (안 보일 때·낭독기용)', '그림 크기', '그림 테두리', '누르면 이동할 주소']),
  fill('링크 주소를 넣으세요', '<a ▢="https://example.com">예시</a>', ['href', 'src', 'alt', 'link']),
  fill('새 탭에서 열리게 하세요', '<a href="https://example.com" target="▢">예시</a>', ['_blank', 'new', 'tab', '_newtab']),
  bug('<img href="cat.jpg" alt="고양이">', 0, '이미지 주소는 href가 아니라 src에 넣어요.'),
  mc('<img src="dog.jpg" alt="강아지"> 에서 dog.jpg 파일이 없으면?', ['깨진 그림 대신 "강아지" 설명이 보일 수 있다', '페이지 전체가 멈춘다', 'dog.jpg 글자가 보인다', '자동으로 다른 그림이 나온다']),
  task('https://www.python.org 로 가는 파이썬 홈 링크를 만드세요', '<a href="https://www.python.org">파이썬 홈</a>', '', check='(()=>{const a=doc.querySelector("a");return !!a&&a.getAttribute("href")==="https://www.python.org"&&a.textContent.trim()==="파이썬 홈"})()'),
  task('src가 https://picsum.photos/100 이고 alt가 랜덤 사진인 이미지를 넣으세요', '<img src="https://picsum.photos/100" alt="랜덤 사진">', '', check='(()=>{const i=doc.querySelector("img");return !!i&&i.getAttribute("src")==="https://picsum.photos/100"&&i.getAttribute("alt")==="랜덤 사진"})()'),
 ]),
 dict(id='ht4', t='목록과 표', ic='<li>', d='항목 나열과 표 만들기', cards=[
  card('순서 없는 목록 ul', '<code>&lt;ul&gt;</code> 안에 <code>&lt;li&gt;</code>를 넣으면 점(•) 목록이 돼요.', '<ul>\n  <li>우유</li>\n  <li>계란</li>\n  <li>빵</li>\n</ul>'),
  card('번호 목록 ol', '<code>&lt;ol&gt;</code>을 쓰면 1, 2, 3 번호가 자동으로 붙어요.', '<ol>\n  <li>물을 끓인다</li>\n  <li>면을 넣는다</li>\n  <li>3분 기다린다</li>\n</ol>'),
  card('표 table', '<code>&lt;table&gt;</code> 안에 행 <code>&lt;tr&gt;</code>, 행 안에 칸 <code>&lt;td&gt;</code>를 넣어요. 머리글 칸은 <code>&lt;th&gt;</code>예요.', '<table border="1">\n  <tr><th>이름</th><th>점수</th></tr>\n  <tr><td>민수</td><td>90</td></tr>\n  <tr><td>지영</td><td>85</td></tr>\n</table>'),
 ], q=[
  mc('번호가 붙는 목록은?', ['<ol>', '<ul>', '<li>', '<nl>'], 'ol은 ordered list(순서 있는 목록)예요.'),
  mc('목록의 각 항목 태그는?', ['<li>', '<item>', '<ol>', '<td>']),
  mc('표에서 한 줄(행)을 만드는 태그는?', ['<tr>', '<td>', '<th>', '<row>'], 'tr은 table row예요.'),
  mc('표의 머리글 칸은?', ['<th>', '<td>', '<thead>만 가능', '<header>']),
  out('<ol>\n  <li>가</li>\n  <li>나</li>\n</ol>', ['1. 가\n2. 나', '• 가\n• 나', '가 나', '1. 나\n2. 가'], '', q='화면에 어떻게 보일까요?'),
  bug('<ul>\n  <li>사과</li>\n  <p>배</p>\n</ul>', 2, 'ul 안에는 li만 넣어야 해요.'),
  fill('점 목록을 만드세요', '<▢>\n  <li>하나</li>\n</ul>', ['ul', 'ol', 'li', 'list']),
  order('표 한 줄을 완성하세요', ['<table>', '  <tr>', '    <td>사과</td>', '    <td>1000원</td>', '  </tr>', '</table>']),
  task('항목 3개가 있는 순서 없는 목록을 만드세요 (내용은 자유)', '<ul>\n  <li>하나</li>\n  <li>둘</li>\n  <li>셋</li>\n</ul>', '', check='doc.querySelectorAll("ul > li").length===3'),
  task('2행 2열 표를 만드세요 (td 4개)', '<table>\n  <tr><td>1</td><td>2</td></tr>\n  <tr><td>3</td><td>4</td></tr>\n</table>', '', check='doc.querySelectorAll("table tr").length===2&&doc.querySelectorAll("table td").length===4'),
 ]),
 dict(id='ht5', t='CSS 시작', ic='{ }', d='색과 글자 꾸미기', cards=[
  card('CSS는 꾸미기 담당', 'HTML이 뼈대라면 CSS는 옷이에요. <code>&lt;style&gt;</code> 안에 <code>선택자 { 속성: 값; }</code> 형태로 써요.', '<style>\n  h1 { color: tomato; }\n  p { font-size: 20px; }\n</style>\n<h1>빨간 제목</h1>\n<p>큰 글씨 문단</p>'),
  card('자주 쓰는 속성', '<code>color</code> 글자색, <code>background-color</code> 배경색, <code>font-size</code> 글자 크기, <code>text-align</code> 정렬, <code>font-weight</code> 굵기.', '<style>\n  body { background-color: #f0f4ff; }\n  h1 { text-align: center; font-weight: bold; }\n</style>\n<h1>가운데 제목</h1>'),
  card('색 표현과 style 속성', '<code>red</code> 같은 이름, <code>#ff0000</code> 같은 16진수, <code>rgb(255, 0, 0)</code> 모두 같은 빨강이에요. 태그에 <code>style=""</code> 속성으로 바로 꾸밀 수도 있어요.', '<p style="color: #2e7d32;">초록 글씨</p>\n<p style="color: rgb(255, 0, 0);">빨간 글씨</p>'),
 ], q=[
  mc('글자색을 바꾸는 속성은?', ['color', 'font-color', 'text-color', 'background-color']),
  mc('CSS 규칙의 올바른 모양은?', ['p { color: red; }', 'p ( color = red )', 'p: color red;', '<p color="red">']),
  mc('글자를 가운데 정렬하려면?', ['text-align: center;', 'align: middle;', 'center: true;', 'text: center;']),
  mc('CSS의 주석은?', ['/* 메모 */', '<!-- 메모 -->', '# 메모', '// 메모'], 'CSS에서 //는 주석이 아니에요.'),
  fill('속성과 값 사이에 들어갈 기호는?', 'h1 { font-size▢ 32px; }', [':', '=', ';', '-']),
  bug('<style>\n  p { color: blue; }\n  h1 { color red; }\n</style>', 2, '속성 이름과 값 사이에 콜론(:)이 빠졌어요.'),
  mc('#000000은 무슨 색일까요?', ['검정', '흰색', '빨강', '파랑'], '#ffffff가 흰색이에요.'),
  out('<style>p { color: green; }</style>\n<p>A</p>\n<h1>B</h1>', ['A만', 'B만', 'A와 B 모두', '없음'], 'p 선택자는 p 태그만 골라요.', q='초록색으로 보이는 글자는?'),
  task('모든 h1의 글자색을 blue로 하고, h1 파란 제목을 넣으세요', '<style>\n  h1 { color: blue; }\n</style>\n<h1>파란 제목</h1>', '', check='(()=>{const h=doc.querySelector("h1");return !!h&&win.getComputedStyle(h).color==="rgb(0, 0, 255)"})()'),
  task('body 배경색을 lightyellow로 바꾸세요', '<style>\n  body { background-color: lightyellow; }\n</style>', '', check='win.getComputedStyle(doc.body).backgroundColor==="rgb(255, 255, 224)"'),
 ]),
 dict(id='ht6', t='박스 모델', ic='[□]', d='여백과 테두리 다루기', cards=[
  card('모든 요소는 상자', '안쪽부터 <b>내용 → padding(안쪽 여백) → border(테두리) → margin(바깥 여백)</b> 순서로 감싸져 있어요.', '<style>\n  .box { padding: 20px; border: 3px solid #333; margin: 30px; background: #ffe; }\n</style>\n<div class="box">상자 안의 글</div>'),
  card('div와 크기', '<code>&lt;div&gt;</code>는 특별한 뜻 없이 영역을 묶는 상자예요. <code>width</code>, <code>height</code>로 크기를, <code>border-radius</code>로 둥근 모서리를 줘요.', '<style>\n  div { width: 120px; height: 80px; background: skyblue; border-radius: 12px; }\n</style>\n<div></div>'),
  card('border 쓰는 법', '<code>border: 두께 모양 색;</code> 예) <code>2px solid red</code>, <code>1px dashed gray</code>.', '<p style="border: 2px dashed gray; padding: 8px;">점선 테두리</p>'),
 ], q=[
  mc('테두리와 내용 사이의 안쪽 여백은?', ['padding', 'margin', 'border', 'gap']),
  mc('다른 요소와의 바깥 여백은?', ['margin', 'padding', 'outline', 'space']),
  mc('모서리를 둥글게 하는 속성은?', ['border-radius', 'corner', 'round', 'border-round']),
  fill('2px 실선 빨간 테두리를 만드세요', 'border: 2px ▢ red;', ['solid', 'line', 'straight', 'full']),
  mc('특별한 뜻 없이 영역을 묶는 상자 태그는?', ['<div>', '<box>', '<area>', '<group>'], '글자 일부만 묶을 땐 <span>을 써요.'),
  mc('padding: 10px 20px; 의 뜻은?', ['위아래 10px, 좌우 20px', '위 10px, 아래 20px', '좌우 10px, 위아래 20px', '모두 30px']),
  bug('div {\n  width: 100;\n  height: 50px;\n}', 1, '0이 아닌 크기에는 px 같은 단위를 꼭 붙여야 해요.'),
  mc('border: 1px solid black; 에서 1px는?', ['테두리 두께', '테두리 길이', '모서리 크기', '여백']),
  task('class가 card인 div를 만들고 padding 16px, 테두리 1px solid gray를 주세요', '<style>\n  .card { padding: 16px; border: 1px solid gray; }\n</style>\n<div class="card">카드</div>', '', check='(()=>{const d=doc.querySelector("div.card");if(!d)return false;const s=win.getComputedStyle(d);return s.paddingTop==="16px"&&s.borderTopWidth==="1px"&&s.borderTopStyle==="solid"})()'),
  task('가로 100px, 세로 100px, 배경 red인 div를 만드세요', '<style>\n  div { width: 100px; height: 100px; background: red; }\n</style>\n<div></div>', '', check='(()=>{const d=doc.querySelector("div");if(!d)return false;const s=win.getComputedStyle(d);return s.width==="100px"&&s.height==="100px"&&s.backgroundColor==="rgb(255, 0, 0)"})()'),
 ]),
 dict(id='ht7', t='클래스와 배치', ic='.cls', d='class, id, flex로 가로 배치', cards=[
  card('class와 id', '여러 요소에 같은 스타일을 줄 땐 <code>class</code>, 하나만 콕 집을 땐 <code>id</code>. CSS에서 class는 <code>.이름</code>, id는 <code>#이름</code>으로 골라요.', '<style>\n  .tag { color: white; background: purple; padding: 2px 8px; }\n  #main { font-size: 24px; }\n</style>\n<p id="main">메인 문장</p>\n<span class="tag">HTML</span> <span class="tag">CSS</span>'),
  card('flex로 가로 배치', '부모에 <code>display: flex;</code>를 주면 자식들이 가로로 나란히 서요. <code>gap</code>으로 간격, <code>justify-content</code>로 정렬해요.', '<style>\n  .row { display: flex; gap: 10px; justify-content: center; }\n  .row div { background: #ddd; padding: 10px; }\n</style>\n<div class="row"><div>1</div><div>2</div><div>3</div></div>'),
  card(':hover', '선택자 뒤에 <code>:hover</code>를 붙이면 마우스를 올렸을 때만 스타일이 바뀌어요. 폰에서는 누르고 있을 때 보여요.', '<style>\n  button:hover { background: gold; }\n</style>\n<button>올려 보세요</button>'),
 ], q=[
  mc('class="red"를 CSS로 고를 때는?', ['.red', '#red', 'red', '*red']),
  mc('id="top"을 CSS로 고를 때는?', ['#top', '.top', 'top', '@top']),
  mc('한 페이지에 여러 번 써도 되는 것은?', ['class', 'id', '둘 다 안 됨', '둘 다 한 번만'], 'id는 페이지에서 하나뿐인 이름이어야 해요.'),
  mc('자식들을 가로로 나란히 놓는 속성은?', ['display: flex;', 'float: row;', 'align: horizontal;', 'display: block;']),
  fill('자식 사이 간격을 12px로', '.menu { display: flex; ▢: 12px; }', ['gap', 'space', 'margin-between', 'spacing']),
  bug('<style>\n  #title { color: red; }\n</style>\n<h1 class="title">제목</h1>', 3, 'CSS는 #title(id)를 고르는데 h1에는 class="title"이 있어요. id="title"로 바꿔야 해요.', q='어느 줄을 고쳐야 할까요?'),
  mc('p.note 선택자가 고르는 것은?', ['class가 note인 p', 'id가 note인 p', 'p 안의 note 태그', '모든 p']),
  mc('justify-content: center; 의 효과는?', ['flex 자식들을 가로 가운데로', '글자를 굵게', '세로 가운데로만', '줄바꿈']),
  task('class가 badge인 span 두 개를 만들고 .badge의 글자색을 red로 하세요', '<style>\n  .badge { color: red; }\n</style>\n<span class="badge">A</span>\n<span class="badge">B</span>', '', check='(()=>{const b=doc.querySelectorAll("span.badge");return b.length>=2&&[...b].every(x=>win.getComputedStyle(x).color==="rgb(255, 0, 0)")})()'),
  task('class가 row인 div 안에 div 3개를 넣고 .row에 display: flex를 주세요', '<style>\n  .row { display: flex; }\n</style>\n<div class="row">\n  <div>1</div><div>2</div><div>3</div>\n</div>', '', check='(()=>{const r=doc.querySelector("div.row");return !!r&&win.getComputedStyle(r).display==="flex"&&r.querySelectorAll(":scope > div").length===3})()'),
 ]),
]

# ------------------------------------------------------------------ JavaScript
JS = [
 dict(id='js1', t='console.log', ic='log', d='JavaScript로 첫 출력', cards=[
  card('첫 출력', 'JavaScript는 웹페이지를 움직이는 언어예요. <code>console.log()</code>로 값을 출력해요. 문장 끝 세미콜론(;)은 붙이는 습관을 들이면 좋아요.', 'console.log("안녕하세요");\nconsole.log("자바스크립트 시작!");'),
  card('문자열과 숫자', '문자열은 따옴표로 감싸고 숫자는 그대로 써요. 쉼표로 여러 값을 넘기면 공백으로 이어서 출력해요.', 'console.log("나이:", 20);\nconsole.log(1, 2, 3);'),
  card('주석', '<code>//</code>는 한 줄 주석, <code>/* */</code>는 여러 줄 주석이에요.', '// 한 줄 주석\n/* 여러 줄\n   주석 */\nconsole.log("주석은 실행되지 않아요");'),
 ], q=[
  mc('JavaScript에서 출력하는 명령은?', ['console.log()', 'print()', 'echo()', 'System.out()'], 'print()는 파이썬이에요.'),
  out('console.log("Hi");', ['Hi', '"Hi"', 'console.log("Hi")', '에러']),
  out('console.log("합:", 5);', ['합: 5', '합:5', '"합:", 5', '합: "5"']),
  mc('JavaScript의 한 줄 주석은?', ['// 메모', '# 메모', '<!-- 메모 -->', '-- 메모']),
  fill('"안녕"을 출력하세요', 'console.▢("안녕");', ['log', 'print', 'write', 'out']),
  bug('console.log("하나");\nconsole.log(둘);\nconsole.log("셋");', 1, '따옴표가 없어서 둘이라는 변수를 찾다가 ReferenceError가 나요.'),
  out('console.log(2 + 3);', ['5', '2 + 3', '23', '에러']),
  order('1단계, 2단계, 3단계 순서로 출력하세요', ['console.log("1단계");', 'console.log("2단계");', 'console.log("3단계");']),
  task('Hello, JS! 를 출력하세요', 'console.log("Hello, JS!");', '', expect='Hello, JS!'),
  task('console.log 한 번으로 점수: 와 100을 쉼표로 함께 출력하세요', 'console.log("점수:", 100);', '', expect='점수: 100', need=[r'console\.log\([^)]*,']),
 ]),
 dict(id='js2', t='변수 let · const', ic='let', d='값을 저장하는 두 가지 방법', cards=[
  card('let과 const', '<code>let</code>은 나중에 바꿀 수 있는 변수, <code>const</code>는 바꿀 수 없는 변수예요. 바꿀 일이 없으면 <code>const</code>부터 쓰는 게 요즘 습관이에요.', 'let score = 10;\nscore = 20;\nconst name = "민수";\nconsole.log(name, score);'),
  card('const는 다시 넣기 금지', 'const에 다시 값을 넣으면 TypeError가 나요.', 'const pi = 3.14;\nconsole.log(pi);\n// pi = 3; // 이 줄의 주석을 풀면 에러'),
  card('자료형과 typeof', '문자열(string), 숫자(number), 참/거짓(boolean), 값 없음(undefined)이 있어요. <code>typeof</code>로 종류를 확인해요.', 'console.log(typeof "a");\nconsole.log(typeof 3);\nconsole.log(typeof true);\nlet x;\nconsole.log(x);'),
 ], q=[
  mc('값을 바꿀 수 없는 변수 선언은?', ['const', 'let', 'var', 'fix']),
  out('let a = 1;\na = 5;\nconsole.log(a);', ['5', '1', '6', '에러']),
  mc('const b = 1; b = 2; 를 실행하면?', ['TypeError 에러', 'b가 2가 된다', 'b가 3이 된다', '아무 일 없다']),
  out('console.log(typeof 42);', ['number', 'string', '42', 'int']),
  out('let x;\nconsole.log(x);', ['undefined', 'null', '0', '에러'], '값을 넣지 않은 변수는 undefined예요.'),
  fill('나중에 바꿀 변수를 만드세요', '▢ city = "부산";\ncity = "서울";', ['let', 'const', 'fix', 'set']),
  out('let a = "3";\nconsole.log(typeof a);', ['string', 'number', '3', 'undefined'], '따옴표로 감싸면 숫자처럼 보여도 문자열이에요.'),
  bug('const count = 0;\ncount = count + 1;\nconsole.log(count);', 0, '값을 바꾸려면 const 대신 let으로 선언해야 해요.', q='어느 줄을 고쳐야 할까요?'),
  task('let으로 변수 hobby에 "독서"를 넣고 출력하세요', 'let hobby = "독서";\nconsole.log(hobby);', '', expect='독서', need=[r'let\s+hobby']),
  task('const로 year에 2026을 넣고 typeof year를 출력하세요', 'const year = 2026;\nconsole.log(typeof year);', '', expect='number', need=[r'const\s+year', 'typeof']),
 ]),
 dict(id='js3', t='연산과 문자열', ic='+ =', d='계산과 템플릿 문자열', cards=[
  card('계산', '<code>+ - * / %</code>를 써요. <code>/</code>는 나누어떨어지지 않으면 소수가 나와요. <code>**</code>는 거듭제곱이에요.', 'console.log(7 / 2);\nconsole.log(7 % 2);\nconsole.log(2 ** 3);'),
  card('문자열 + 는 이어 붙이기', '문자열과 숫자를 <code>+</code>하면 숫자가 문자열로 바뀌어 붙어요. <code>"5" + 1</code>은 <code>"51"</code>! 숫자로 바꾸려면 <code>Number()</code>를 써요.', 'console.log("5" + 1);\nconsole.log(Number("5") + 1);'),
  card('템플릿 문자열', '백틱(`)으로 감싸고 <code>${변수}</code>를 쓰면 값이 들어가요. 파이썬의 f-문자열과 같은 역할이에요.', 'const name = "지영";\nconst age = 30;\nconsole.log(`${name}님은 ${age}살`);'),
 ], q=[
  out('console.log(10 % 3);', ['1', '3', '3.33', '0'], '10을 3으로 나눈 나머지는 1이에요.'),
  out('console.log(7 / 2);', ['3.5', '3', '4', '3.0'], 'JavaScript의 /는 소수까지 계산해요.'),
  out('console.log("5" + 1);', ['51', '6', '에러', '"5"1'], '문자열이 하나라도 있으면 +는 이어 붙이기예요.'),
  out('console.log("5" - 1);', ['4', '51', 'NaN', '에러'], '-는 문자열에 없는 연산이라 숫자로 바꿔 계산해요. 헷갈리니 Number()로 바꾸는 습관을 들여요.'),
  out('const n = 3;\nconsole.log(`값은 ${n * 2}`);', ['값은 6', '값은 ${n * 2}', '값은 n * 2', '값은 3']),
  mc('템플릿 문자열을 감싸는 기호는?', ['` (백틱)', '" (큰따옴표)', "' (작은따옴표)", '# (샵)'], '키보드 숫자 1 왼쪽에 있는 기호예요.'),
  out('console.log(2 ** 4);', ['16', '8', '6', '24']),
  bug('const a = "10";\nconst b = 5;\nconsole.log(a + b); // 15가 나와야 함', 0, 'a가 문자열 "10"이라 결과가 "105"가 돼요. const a = 10; 처럼 숫자로 써야 해요.', q='어느 줄을 고쳐야 할까요?'),
  task('price와 qty를 곱한 총액을 출력하세요', 'const price = 4500;\nconst qty = 2;\nconsole.log(price * qty);', '', start='const price = 4500;\nconst qty = 2;\n', expect='9000'),
  task('const name = "하나"; 를 쓰고 템플릿 문자열로 하나님 안녕 을 출력하세요', 'const name = "하나";\nconsole.log(`${name}님 안녕`);', '', expect='하나님 안녕', need=['`']),
 ]),
 dict(id='js4', t='조건문 if', ic='if ( )', d='조건에 따라 다르게 실행하기', cards=[
  card('비교는 ===', '<code>===</code> 같다, <code>!==</code> 다르다, <code>&gt; &lt; &gt;= &lt;=</code>. <code>==</code>는 자료형을 멋대로 바꿔 비교해서 헷갈리니 <code>===</code>를 쓰세요.', 'console.log(3 === 3);\nconsole.log(3 === "3");\nconsole.log(3 == "3");'),
  card('if / else if / else', '조건은 <code>( )</code> 안에, 실행할 코드는 <code>{ }</code> 안에 써요.', 'const score = 85;\nif (score >= 90) {\n  console.log("A");\n} else if (score >= 80) {\n  console.log("B");\n} else {\n  console.log("C");\n}'),
  card('&& || !', '<code>&&</code> 그리고, <code>||</code> 또는, <code>!</code> 반대예요.', 'const age = 25;\nconsole.log(age >= 20 && age < 30);\nconsole.log(!true);'),
 ], q=[
  out('console.log(5 === "5");', ['false', 'true', '5', '에러'], '===는 자료형까지 같아야 참이에요.'),
  out('console.log(5 == "5");', ['true', 'false', '에러', 'undefined'], '==는 자료형을 바꿔서 비교해서 참이 돼요. 그래서 ===를 권해요.'),
  mc('자료형까지 엄격하게 비교하는 연산자는?', ['===', '==', '=', '!==']),
  out('const x = 7;\nif (x > 10) {\n  console.log("크다");\n} else {\n  console.log("작다");\n}', ['작다', '크다', '크다\n작다', '에러']),
  out('console.log(true && false);', ['false', 'true', 'undefined', '에러']),
  out('console.log(!true);', ['false', 'true', '!true', '에러']),
  fill('코드 블록을 여세요', 'if (x > 0) ▢\n  console.log("양수");\n}', ['{', '(', ':', '[']),
  bug('const n = 4;\nif n % 2 === 0 {\n  console.log("짝수");\n}', 1, 'JavaScript는 조건을 괄호 ( )로 감싸야 해요.'),
  task('temp가 30 이상이면 더워요, 아니면 괜찮아요를 출력하세요', 'const temp = 25;\nif (temp >= 30) {\n  console.log("더워요");\n} else {\n  console.log("괜찮아요");\n}', '', start='const temp = 25;\n', expect='괜찮아요', need=['if', 'else']),
  task('n이 짝수면 짝수, 홀수면 홀수를 출력하세요', 'const n = 7;\nif (n % 2 === 0) {\n  console.log("짝수");\n} else {\n  console.log("홀수");\n}', '', start='const n = 7;\n', expect='홀수', need=['%', 'if']),
 ]),
 dict(id='js5', t='반복문', ic='for', d='for와 while로 반복하기', cards=[
  card('for 문', '<code>for (시작; 조건; 증가) { }</code> 형태예요. <code>i++</code>는 i를 1 늘린다는 뜻이에요.', 'for (let i = 0; i < 3; i++) {\n  console.log("반복", i);\n}'),
  card('누적하기', '<code>total += i</code>는 <code>total = total + i</code>의 줄임말이에요.', 'let total = 0;\nfor (let i = 1; i <= 10; i++) {\n  total += i;\n}\nconsole.log(total);'),
  card('while과 break', '<code>while (조건)</code>은 조건이 참인 동안 반복해요. <code>break</code>는 반복을 바로 멈춰요.', 'let n = 3;\nwhile (n > 0) {\n  console.log(n);\n  n--;\n}\nconsole.log("발사!");'),
 ], q=[
  out('for (let i = 0; i < 3; i++) {\n  console.log(i);\n}', ['0\n1\n2', '1\n2\n3', '0\n1\n2\n3', '3']),
  out('for (let i = 1; i <= 3; i++) {\n  console.log(i * 10);\n}', ['10\n20\n30', '1\n2\n3', '10\n20', '30']),
  mc('i++ 의 뜻은?', ['i를 1 늘린다', 'i를 2배로 한다', 'i를 출력한다', 'i를 0으로 만든다']),
  out('let s = 0;\nfor (let i = 1; i <= 4; i++) {\n  s += i;\n}\nconsole.log(s);', ['10', '4', '15', '0']),
  out('let i = 0;\nwhile (i < 3) {\n  i++;\n}\nconsole.log(i);', ['3', '2', '0', '무한 반복']),
  out('for (let i = 0; i < 10; i++) {\n  if (i === 3) break;\n  console.log(i);\n}', ['0\n1\n2', '0\n1\n2\n3', '3', '0부터 9까지 전부']),
  fill('5번 반복하세요', 'for (let i = 0; i ▢ 5; i++) {', ['<', '<=', '>', '==='], '0, 1, 2, 3, 4 다섯 번이에요. <=를 쓰면 6번이 돼요.'),
  mc('for (let i = 0; i < 3; i--) 의 문제는?', ['i가 줄어들어 끝나지 않는다', '3번만 반복한다', '문법 에러', '한 번도 돌지 않는다']),
  task('for로 JS를 3번 출력하세요', 'for (let i = 0; i < 3; i++) {\n  console.log("JS");\n}', '', expect='JS\nJS\nJS', need=['for']),
  task('1부터 100까지의 합을 출력하세요', 'let total = 0;\nfor (let i = 1; i <= 100; i++) {\n  total += i;\n}\nconsole.log(total);', '', expect='5050', need=['for|while']),
 ]),
 dict(id='js6', t='배열', ic='[ ]', d='여러 값을 순서대로 담기', cards=[
  card('배열 만들기', '<code>[ ]</code> 안에 값을 넣어요. 번호는 0부터, 개수는 <code>.length</code>예요.', 'const fruits = ["사과", "바나나", "포도"];\nconsole.log(fruits[0]);\nconsole.log(fruits.length);'),
  card('추가와 꺼내기', '<code>push()</code>는 맨 뒤에 추가, <code>pop()</code>은 맨 뒤를 꺼내서 지워요. const 배열도 안의 내용은 바꿀 수 있어요.', 'const a = [1, 2];\na.push(3);\nconsole.log(a);\na.pop();\nconsole.log(a);'),
  card('하나씩 꺼내기', '<code>for (const 값 of 배열)</code>로 값을 하나씩 꺼내요.', 'const nums = [3, 5, 7];\nfor (const n of nums) {\n  console.log(n);\n}'),
 ], q=[
  out('const a = [10, 20, 30];\nconsole.log(a[1]);', ['20', '10', '30', 'undefined']),
  out('const a = [10, 20, 30];\nconsole.log(a.length);', ['3', '2', '30', '4']),
  out('const a = [1, 2];\na.push(9);\nconsole.log(a);', ['[1, 2, 9]', '[9, 1, 2]', '[1, 2]', '3']),
  out('const a = ["x", "y"];\nconsole.log(a[2]);', ['undefined', 'y', '에러', 'null'], '없는 번호는 에러 대신 undefined예요. 파이썬은 에러가 나요.'),
  fill('배열 뒤에 추가하세요', 'list.▢("새 항목");', ['push', 'append', 'add', 'insert'], 'append는 파이썬이에요.'),
  mc('배열 마지막 값을 꺼내 지우는 메서드는?', ['pop()', 'push()', 'shift()', 'last()']),
  order('배열의 값을 하나씩 출력하세요', ['const names = ["가", "나"];', 'for (const n of names) {', '  console.log(n);', '}']),
  out('const a = [1, 2, 3];\nconsole.log(a.includes(2));', ['true', 'false', '2', '1'], 'includes는 값이 들어 있는지 확인해요.'),
  task('배열 [4, 9, 2]의 길이를 출력하세요', 'const a = [4, 9, 2];\nconsole.log(a.length);', '', expect='3', need=['length']),
  task('빈 배열을 만들고 push로 "a", "b"를 넣은 뒤 출력하세요', 'const arr = [];\narr.push("a");\narr.push("b");\nconsole.log(arr);', '', expect="['a', 'b']", need=['push']),
 ]),
 dict(id='js7', t='함수', ic='( ) =>', d='function과 화살표 함수', cards=[
  card('function', '<code>function 이름(매개변수) { }</code>로 만들고 <code>이름()</code>으로 불러요. <code>return</code>으로 값을 돌려줘요.', 'function add(a, b) {\n  return a + b;\n}\nconsole.log(add(2, 3));'),
  card('화살표 함수', '<code>const 이름 = (매개변수) =&gt; 값;</code>처럼 짧게 쓸 수 있어요. 요즘 코드에서 아주 많이 보여요.', 'const double = (x) => x * 2;\nconsole.log(double(21));'),
  card('return이 없으면', 'return이 없는 함수는 <code>undefined</code>를 돌려줘요.', 'function hi() {\n  console.log("hi");\n}\nconst r = hi();\nconsole.log(r);'),
 ], q=[
  mc('함수를 만드는 키워드는?', ['function', 'def', 'func', 'fn'], 'def는 파이썬이에요.'),
  out('function sq(x) {\n  return x * x;\n}\nconsole.log(sq(4));', ['16', '8', '4', 'undefined']),
  out('const f = (a, b) => a - b;\nconsole.log(f(10, 3));', ['7', '13', '-7', 'undefined']),
  out('function f() {\n  console.log("A");\n}\nconsole.log("B");', ['B', 'A\nB', 'A', 'B\nA'], '함수는 부르지 않으면 실행되지 않아요.'),
  out('function f() {}\nconsole.log(f());', ['undefined', 'null', '0', '에러']),
  fill('절반을 돌려주세요', 'function half(n) {\n  ▢ n / 2;\n}', ['return', 'print', 'give', '=>']),
  bug('function hello() {\n  console.log("안녕");\n}\nhello;', 3, '함수를 실행하려면 hello()처럼 괄호를 붙여야 해요.'),
  order('함수를 만들고 부르세요', ['function cheer(name) {', '  console.log(name + " 화이팅!");', '}', 'cheer("민수");']),
  task('두 수를 곱해 돌려주는 함수 mul을 만들고 console.log(mul(6, 7))을 실행하세요', 'function mul(a, b) {\n  return a * b;\n}\nconsole.log(mul(6, 7));', '', expect='42', need=['mul'], test='console.log(mul(-2, 5), mul(0, 9))', testOut='-10 0'),
  task('화살표 함수 greet를 만들어 greet("민수")로 안녕, 민수를 출력하세요', 'const greet = (name) => console.log(`안녕, ${name}`);\ngreet("민수");', '', expect='안녕, 민수', need=['=>'], test='greet("지영")', testOut='안녕, 지영'),
 ]),
 dict(id='js8', t='웹페이지 움직이기', ic='DOM', d='버튼을 누르면 바뀌는 페이지', lang='html', cards=[
  card('요소 고르기', '<code>document.querySelector("선택자")</code>로 HTML 요소를 고르고, <code>textContent</code>로 글자를 바꿔요. 선택자는 CSS와 똑같이 써요.', '<h1 id="title">원래 제목</h1>\n<script>\n  const t = document.querySelector("#title");\n  t.textContent = "자바스크립트가 바꾼 제목";\n</script>'),
  card('스타일 바꾸기', '<code>요소.style.속성 = 값</code>. CSS의 <code>background-color</code>는 <code>backgroundColor</code>처럼 붙여 써요.', '<p id="msg">색이 바뀌는 문장</p>\n<script>\n  document.querySelector("#msg").style.color = "crimson";\n</script>'),
  card('버튼 클릭', '<code>addEventListener("click", 함수)</code>로 클릭했을 때 할 일을 정해요. 아래 미리보기에서 버튼을 눌러 보세요.', '<button id="btn">눌러 보세요</button>\n<p id="out">0</p>\n<script>\n  let n = 0;\n  document.querySelector("#btn").addEventListener("click", () => {\n    n++;\n    document.querySelector("#out").textContent = n;\n  });\n</script>'),
 ], q=[
  mc('id가 box인 요소를 고르는 코드는?', ['document.querySelector("#box")', 'document.querySelector("box")', 'document.get("box")', 'select("#box")']),
  mc('요소의 글자를 바꾸는 속성은?', ['textContent', 'text()', 'value()', 'write']),
  mc('클릭했을 때 할 일을 정하는 메서드는?', ['addEventListener', 'onClickDo', 'listen', 'addClick']),
  fill('클릭 이벤트를 연결하세요', 'btn.addEventListener("▢", () => { });', ['click', 'press', 'tap', 'onclick']),
  mc('CSS background-color를 JavaScript에서 바꿀 때 쓰는 이름은?', ['backgroundColor', 'background-color', 'bgColor', 'background_color']),
  bug('<p id="hi">안녕</p>\n<script>\n  document.querySelector("hi").textContent = "반가워";\n</script>', 2, 'id로 고를 때는 "#hi"처럼 #을 붙여야 해요.'),
  out('<p id="p">A</p>\n<script>\n  const p = document.querySelector("#p");\n  p.textContent = p.textContent + "B";\n</script>', ['AB', 'A', 'B', 'BA'], '', q='실행 후 p에 보이는 글자는?'),
  order('버튼을 누르면 콘솔에 시작!이 찍히게 하세요', ['<button id="go">시작</button>', '<script>', '  document.querySelector("#go").addEventListener("click", () => {', '    console.log("시작!");', '  });', '</script>']),
  task('script로 h1의 글자를 시작!으로 바꾸세요', '<h1 id="t">준비</h1>\n<script>\n  document.querySelector("#t").textContent = "시작!";\n</script>', '', start='<h1 id="t">준비</h1>\n<script>\n  \n</script>', check='(doc.querySelector("h1")||{}).textContent==="시작!"', need=['querySelector']),
  task('버튼을 누르면 p#out의 글자가 눌렀다로 바뀌게 하세요', '<button id="b">버튼</button>\n<p id="out">아직</p>\n<script>\n  document.querySelector("#b").addEventListener("click", () => {\n    document.querySelector("#out").textContent = "눌렀다";\n  });\n</script>', '', start='<button id="b">버튼</button>\n<p id="out">아직</p>\n<script>\n  \n</script>', check='(()=>{const b=doc.querySelector("#b");if(!b)return false;b.click();return (doc.querySelector("#out")||{}).textContent==="눌렀다"})()', need=['addEventListener|onclick']),
 ]),
]

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deep_code.py'), encoding='utf-8').read())
PY += PYX
HT += HTX
JS += JSX

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expl.py'), encoding='utf-8').read())

COURSES = [
 dict(id='py', name='Python', lang='python', g='py', d='입문자에게 가장 쉬운 언어. 데이터·자동화·AI까지', units=PY),
 dict(id='ht', name='HTML·CSS', lang='html', g='ht', d='웹페이지의 뼈대와 옷. 결과가 바로 눈에 보여요', units=HT),
 dict(id='js', name='JavaScript', lang='javascript', g='js', d='웹페이지를 움직이는 언어', units=JS),
 dict(id='sc', name='보안', lang='javascript', g='sc', d='해킹은 어떻게 일어나고 어떻게 막을까. XSS·인젝션·비밀번호·개인정보', units=SEC),
 dict(id='ap', name='앱개발', lang='javascript', g='ap', d='앱의 구조, API, 직접 만드는 작은 앱, Git과 출시까지', units=APP),
]

for _c in COURSES:
    for _u in _c['units']:
        for _i, _q in enumerate(_u['q']):
            if not (_q.get('e') or '').strip() and EXPL.get(f"{_u['id']}:{_i}"):
                _q['e'] = EXPL[f"{_u['id']}:{_i}"]
here = os.path.dirname(os.path.abspath(__file__))
dst = os.path.join(here, '..', 'www', 'course.js')
n = sum(len(u['q']) for c in COURSES for u in c['units'])
with open(dst, 'w', encoding='utf-8') as f:
    f.write('// 자동 생성: content/course.py 를 고친 뒤 python3 content/course.py\nwindow.COURSES=' + json.dumps(COURSES, ensure_ascii=False) + ';\n')
print('units', sum(len(c['units']) for c in COURSES), 'questions', n)
