# 심화 단원: course.py 안에서 exec로 불러와요 (mc, out, fill, order, bug, task, card 사용)

PYX = [
 dict(id='py9', t='딕셔너리', ic='{ : }', d='이름표(키)로 값을 찾는 자료형', cards=[
  card('키와 값의 짝', '리스트는 <b>순서 번호</b>로 값을 찾지만, 딕셔너리는 <b>이름표(키)</b>로 찾아요. 사전에서 단어(키)로 뜻(값)을 찾는 것과 같아요. <code>{키: 값, 키: 값}</code> 모양이고, <code>사전[키]</code>로 꺼내요.', 'student = {"name": "민수", "age": 15, "score": 92}\nprint(student["name"])\nprint(student["score"])'),
  card('추가·수정·삭제', '없는 키에 값을 넣으면 <b>추가</b>, 있는 키에 넣으면 <b>수정</b>이에요. <code>del</code>로 지워요. 없는 키를 <code>[ ]</code>로 꺼내면 에러가 나니, 안전하게 꺼낼 땐 <code>.get(키, 기본값)</code>을 써요.', 'p = {"name": "지영"}\np["age"] = 16      # 추가\np["name"] = "지영!" # 수정\nprint(p)\nprint(p.get("email", "없음"))'),
  card('딕셔너리 돌기', '<code>for k, v in 사전.items():</code>로 키와 값을 함께 꺼내요. <code>.keys()</code>는 키만, <code>.values()</code>는 값만 줘요.', 'price = {"사과": 1000, "배": 3000, "귤": 500}\nfor fruit, won in price.items():\n    print(fruit, won, "원")\nprint(sum(price.values()))'),
  card('리스트 안의 딕셔너리', '실제 데이터는 "딕셔너리들의 리스트"인 경우가 많아요. 웹에서 받는 JSON 데이터도 이 모양이에요.', 'users = [\n    {"name": "민수", "level": 3},\n    {"name": "지영", "level": 5},\n]\nfor u in users:\n    print(u["name"], "레벨", u["level"])'),
 ], q=[
  out('d = {"a": 1, "b": 2}\nprint(d["b"])', ['2', '1', 'b', '에러']),
  out('d = {"x": 10}\nd["x"] = 20\nprint(d["x"])', ['20', '10', '30', '에러'], '같은 키에 넣으면 값이 바뀌어요.'),
  out('d = {"x": 1}\nprint(d.get("y", 0))', ['0', '1', 'None', '에러'], 'get은 없는 키면 기본값을 줘요.'),
  mc('딕셔너리에서 키와 값을 함께 꺼내며 반복할 때 쓰는 것은?', ['.items()', '.keys()', '.values()', '.list()']),
  fill('키 "city"에 "서울"을 넣으세요', 'info = {}\ninfo[▢] = "서울"', ['"city"', 'city', '[city]', '.city']),
  bug('menu = {"라면": 3000}\nprint(menu["김밥"])', 1, '없는 키를 [ ]로 꺼내면 KeyError가 나요. menu.get("김밥")을 쓰면 안전해요.'),
  task('딕셔너리 book = {"title": "어린왕자", "page": 120} 을 만들고 title 값을 출력하세요', 'book = {"title": "어린왕자", "page": 120}\nprint(book["title"])', '', expect='어린왕자', need=[r'\{']),
 ]),
 dict(id='py10', t='클래스와 객체', ic='class', d='설계도(클래스)로 물건(객체) 만들기', cards=[
  card('객체란?', '<b>객체(object)</b>는 "데이터(속성)와 그 데이터로 하는 행동(메서드)"을 하나로 묶은 거예요. 강아지 객체라면 이름·나이(속성)와 짖기(메서드)를 함께 가져요. 사실 파이썬의 문자열·리스트도 모두 객체라서 <code>"hi".upper()</code>처럼 점(.)으로 메서드를 불렀던 거예요.', 'word = "hello"\nprint(word.upper())   # 문자열 객체의 메서드\nnums = [3, 1, 2]\nnums.sort()           # 리스트 객체의 메서드\nprint(nums)'),
  card('클래스는 설계도', '<b>클래스</b>는 객체를 찍어 내는 설계도(붕어빵 틀)이고, 그 틀로 만든 하나하나가 <b>인스턴스</b>(객체)예요. <code>__init__</code>은 객체가 만들어질 때 자동으로 실행돼 처음 값을 넣어 줘요. <code>self</code>는 "지금 만들어지는 바로 그 객체"를 가리켜요.', 'class Dog:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n\na = Dog("초코", 3)\nb = Dog("콩이", 1)\nprint(a.name, a.age)\nprint(b.name, b.age)'),
  card('메서드: 객체의 행동', '클래스 안의 함수를 <b>메서드</b>라고 해요. 첫 번째 매개변수는 항상 <code>self</code>이고, 이걸로 자기 속성을 읽고 바꿔요.', 'class Account:\n    def __init__(self, owner):\n        self.owner = owner\n        self.money = 0\n    def deposit(self, amount):\n        self.money += amount\n        print(self.owner, "잔액:", self.money)\n\nacc = Account("민수")\nacc.deposit(1000)\nacc.deposit(500)'),
  card('상속: 설계도 물려받기', '기존 클래스를 물려받아 새 클래스를 만들면 공통 코드를 다시 쓰지 않아도 돼요. 괄호 안에 부모 클래스를 적고, 필요한 메서드만 새로 정의(오버라이딩)해요.', 'class Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        print(self.name, "...")\n\nclass Cat(Animal):\n    def speak(self):\n        print(self.name, "야옹")\n\nAnimal("동물").speak()\nCat("나비").speak()'),
  card('왜 객체를 쓸까?', '게임 캐릭터 100명, 회원 1만 명처럼 <b>같은 구조의 데이터가 많을 때</b> 클래스 하나로 관리하면 코드가 짧고 실수가 줄어요. 데이터와 그걸 다루는 코드가 한곳에 있어서 고칠 곳을 찾기도 쉬워요. 이런 방식을 <b>객체지향 프로그래밍(OOP)</b>이라고 해요.'),
 ], q=[
  mc('클래스와 객체의 관계로 알맞은 것은?', ['클래스는 설계도, 객체는 그 설계도로 만든 실물', '클래스와 객체는 같은 말', '객체가 클래스를 만든다', '클래스는 숫자, 객체는 문자']),
  mc('객체가 만들어질 때 자동으로 실행되는 메서드는?', ['__init__', '__start__', 'main', 'self']),
  out('class P:\n    def __init__(self, n):\n        self.n = n\np = P(7)\nprint(p.n)', ['7', 'n', 'P', '에러']),
  out('class C:\n    def __init__(self):\n        self.v = 0\n    def up(self):\n        self.v += 1\nc = C()\nc.up()\nc.up()\nprint(c.v)', ['2', '1', '0', '에러']),
  out('class A:\n    def hi(self):\n        print("A")\nclass B(A):\n    def hi(self):\n        print("B")\nB().hi()', ['B', 'A', 'A\nB', '에러'], '자식 클래스에서 다시 정의한 메서드가 쓰여요.'),
  fill('메서드의 첫 번째 매개변수를 채우세요', 'class Cat:\n    def meow(▢):\n        print("야옹")', ['self', 'this', 'cat', 'me']),
  bug('class Car:\n    def __init__(self, color):\n        color = color\ncar = Car("red")\nprint(car.color)', 2, 'self.color = color 로 써야 객체에 저장돼요.'),
  task('name 속성을 가진 클래스 Hero를 만들고 Hero("하나")의 name을 출력하세요', 'class Hero:\n    def __init__(self, name):\n        self.name = name\n\nh = Hero("하나")\nprint(h.name)', '', expect='하나', need=[r'class\s+Hero', '__init__'], test='print(Hero("둘").name)', testOut='둘'),
 ]),
 dict(id='py11', t='예외 처리', ic='try', d='에러가 나도 프로그램이 멈추지 않게', cards=[
  card('에러의 종류', '숫자를 0으로 나누면 <code>ZeroDivisionError</code>, 숫자가 아닌 글자를 int로 바꾸면 <code>ValueError</code>, 없는 키를 꺼내면 <code>KeyError</code>가 나요. 에러 메시지 마지막 줄의 이름을 읽는 습관이 디버깅의 시작이에요.'),
  card('try와 except', '에러가 날 수 있는 코드를 <code>try</code>에 넣고, 에러가 나면 <code>except</code>에서 처리해요. 프로그램이 멈추지 않고 다음 줄로 계속 가요.', 'try:\n    n = int("열")\n    print(n)\nexcept ValueError:\n    print("숫자로 바꿀 수 없어요")\nprint("프로그램은 계속돼요")'),
  card('else와 finally', '<code>else</code>는 에러가 없을 때만, <code>finally</code>는 에러가 있든 없든 마지막에 항상 실행돼요. 파일 닫기, 연결 끊기 같은 정리 작업을 finally에 둬요.', 'for x in [2, 0]:\n    try:\n        r = 10 / x\n    except ZeroDivisionError:\n        print("0으로 나눌 수 없어요")\n    else:\n        print("결과", r)\n    finally:\n        print("---")'),
  card('일부러 에러 내기: raise', '잘못된 값이 들어오면 <code>raise</code>로 직접 에러를 내서 문제를 일찍 알려요. 보안에서도 "이상한 입력은 초기에 거절"이 기본이에요.', 'def set_age(age):\n    if age < 0:\n        raise ValueError("나이는 음수일 수 없어요")\n    return age\n\ntry:\n    set_age(-5)\nexcept ValueError as e:\n    print("에러:", e)'),
 ], q=[
  mc('int("abc")를 실행하면 나는 에러는?', ['ValueError', 'KeyError', 'ZeroDivisionError', 'IndexError']),
  out('try:\n    print(1/0)\nexcept ZeroDivisionError:\n    print("X")', ['X', '0', '에러로 멈춤', '1']),
  out('try:\n    a = 5\nexcept:\n    print("E")\nelse:\n    print("OK")', ['OK', 'E', 'E\nOK', '아무것도 안 나옴']),
  out('try:\n    x = 1/0\nexcept ZeroDivisionError:\n    print("A")\nfinally:\n    print("B")', ['A\nB', 'B', 'A', 'B\nA']),
  fill('에러가 있든 없든 항상 실행되는 블록', 'try:\n    pass\n▢:\n    print("정리")', ['finally', 'else', 'always', 'end']),
  mc('잘못된 입력에 직접 에러를 일으키는 키워드는?', ['raise', 'throw', 'error', 'except']),
  task('try/except로 int("오")에서 나는 ValueError를 잡아 변환 실패 를 출력하세요', 'try:\n    int("오")\nexcept ValueError:\n    print("변환 실패")', '', expect='변환 실패', need=['try', 'except']),
 ]),
]

HTX = [
 dict(id='ht8', t='폼과 입력 요소', ic='<form>', d='입력창, 셀렉트박스, 체크박스, 라디오, 버튼', cards=[
  card('폼은 입력을 모으는 상자', '<code>&lt;form&gt;</code> 안에 입력 요소를 넣어요. 각 입력에는 <code>&lt;label&gt;</code>을 붙여야 화면 낭독기 사용자도 무엇을 입력하는지 알 수 있고, 라벨을 눌러도 입력칸이 선택돼요. <code>for</code>와 입력의 <code>id</code>를 같게 맞춰요.', '<form>\n  <label for="nm">이름</label>\n  <input id="nm" type="text" placeholder="홍길동">\n  <label for="em">이메일</label>\n  <input id="em" type="email">\n  <button>보내기</button>\n</form>'),
  card('input의 type', '<code>type</code> 하나로 모양과 키보드가 바뀌어요. <code>text</code>(글자), <code>password</code>(가려짐), <code>number</code>(숫자), <code>email</code>(이메일 형식 검사), <code>date</code>(달력), <code>range</code>(슬라이더), <code>color</code>(색 선택). 모바일에서는 type에 맞는 키보드가 떠요.', '<input type="password" placeholder="비밀번호"><br>\n<input type="number" min="1" max="10" value="3"><br>\n<input type="date"><br>\n<input type="range" min="0" max="100"><br>\n<input type="color" value="#ff6600">'),
  card('셀렉트박스(select)', '여러 선택지 중 하나를 고르는 드롭다운이에요. <code>&lt;select&gt;</code> 안에 <code>&lt;option&gt;</code>을 넣어요. 화면에 보이는 글자와 실제로 전송되는 <code>value</code>는 다를 수 있어요. <code>selected</code>는 처음 선택된 항목, <code>&lt;optgroup&gt;</code>은 항목 묶음이에요.', '<label for="city">지역</label>\n<select id="city">\n  <option value="">선택하세요</option>\n  <optgroup label="수도권">\n    <option value="seoul" selected>서울</option>\n    <option value="incheon">인천</option>\n  </optgroup>\n  <option value="busan">부산</option>\n</select>'),
  card('체크박스와 라디오', '<b>체크박스</b>는 여러 개를 동시에 고를 수 있고, <b>라디오</b>는 같은 <code>name</code>끼리 하나만 고를 수 있어요. <code>checked</code>로 처음부터 선택해 둘 수 있어요.', '<p>관심사 (여러 개)</p>\n<label><input type="checkbox" checked> 코딩</label>\n<label><input type="checkbox"> 게임</label>\n<p>학년 (하나만)</p>\n<label><input type="radio" name="grade"> 1학년</label>\n<label><input type="radio" name="grade" checked> 2학년</label>'),
  card('textarea와 검사 속성', '여러 줄 입력은 <code>&lt;textarea&gt;</code>예요. <code>required</code>(필수), <code>minlength</code>·<code>maxlength</code>(글자 수), <code>min</code>·<code>max</code>(숫자 범위), <code>pattern</code>(정규식)으로 브라우저가 먼저 입력을 검사해요. 단, 이런 검사는 사용자가 쉽게 우회할 수 있어서 <b>서버에서도 반드시 다시 검사</b>해야 해요(보안 코스 참고).', '<form>\n  <textarea rows="3" placeholder="자기소개" maxlength="100"></textarea><br>\n  <input required placeholder="필수 입력">\n  <button>제출</button>\n</form>'),
 ], q=[
  mc('드롭다운 목록을 만드는 태그는?', ['<select>', '<dropdown>', '<list>', '<input type="list">']),
  mc('select 안의 각 선택지를 만드는 태그는?', ['<option>', '<item>', '<li>', '<choice>']),
  mc('여러 개 중 하나만 고르게 하려면?', ['같은 name을 가진 radio', 'checkbox 여러 개', 'select multiple', 'textarea']),
  mc('입력한 글자를 ●●●로 가리는 type은?', ['password', 'hidden', 'secret', 'text']),
  fill('처음부터 선택된 option으로 만드세요', '<select>\n  <option>A</option>\n  <option ▢>B</option>\n</select>', ['selected', 'checked', 'active', 'default']),
  fill('label을 input과 연결하세요', '<label ▢="age">나이</label>\n<input id="age">', ['for', 'id', 'name', 'link']),
  bug('<label><input type="radio" name="a"> 예</label>\n<label><input type="radio" name="b"> 아니오</label>', 1, '같은 그룹이 되려면 name이 같아야 해요(name="a").', q='둘 중 하나만 선택되게 하고 싶어요. 잘못된 줄은?'),
  task('id가 food인 select에 option 세 개(김밥, 라면, 떡볶이)를 만드세요', '<select id="food">\n  <option>김밥</option>\n  <option>라면</option>\n  <option>떡볶이</option>\n</select>', '', check='(doc.querySelectorAll("#food option")||[]).length>=3', need=['<select', '<option']),
 ]),
]

JSX = [
 dict(id='js9', t='객체(Object)', ic='{ }', d='속성과 메서드를 한 묶음으로', cards=[
  card('객체 리터럴', 'JavaScript의 <b>객체</b>는 <code>{ 키: 값 }</code> 묶음이에요. 값은 <code>객체.키</code>(점 표기)나 <code>객체["키"]</code>(대괄호 표기)로 꺼내요. 키 이름이 변수에 들어 있을 땐 대괄호를 써요.', 'const user = { name: "민수", age: 15, admin: false };\nconsole.log(user.name);\nconsole.log(user["age"]);\nconst key = "admin";\nconsole.log(user[key]);'),
  card('바꾸기·추가·삭제', '<code>const</code>로 만든 객체도 <b>속성은 바꿀 수 있어요</b>. const는 "다른 객체로 바꿔치기"만 막아요. 없는 키에 넣으면 추가, <code>delete</code>로 삭제해요.', 'const car = { color: "red" };\ncar.color = "blue";  // 수정\ncar.speed = 100;     // 추가\ndelete car.speed;    // 삭제\nconsole.log(car);'),
  card('메서드와 this', '함수를 값으로 가진 속성이 <b>메서드</b>예요. 메서드 안의 <code>this</code>는 그 메서드를 부른 객체를 가리켜요.', 'const counter = {\n  count: 0,\n  up() {\n    this.count++;\n    console.log("지금", this.count);\n  }\n};\ncounter.up();\ncounter.up();'),
  card('객체 다루기 도구', '<code>Object.keys()</code>는 키 배열, <code>Object.values()</code>는 값 배열, <code>Object.entries()</code>는 [키, 값] 배열을 줘요. <b>구조 분해</b>로 필요한 속성만 꺼내고, <b>스프레드(...)</b>로 복사·합치기를 해요.', 'const p = { name: "지영", city: "부산", job: "개발자" };\nconsole.log(Object.keys(p));\nconst { name, city } = p;\nconsole.log(name, city);\nconst p2 = { ...p, city: "서울" };\nconsole.log(p2.city, p.city);'),
  card('클래스로 객체 찍어 내기', '같은 모양의 객체를 많이 만들 땐 <code>class</code>를 써요. <code>constructor</code>가 처음 값을 넣고, <code>new</code>로 인스턴스를 만들어요. 파이썬의 <code>__init__</code>과 <code>self</code>가 JS에선 <code>constructor</code>와 <code>this</code>예요.', 'class Monster {\n  constructor(name, hp) {\n    this.name = name;\n    this.hp = hp;\n  }\n  hit(d) {\n    this.hp -= d;\n    console.log(`${this.name} HP ${this.hp}`);\n  }\n}\nconst m = new Monster("슬라임", 30);\nm.hit(10);\nm.hit(5);'),
  card('참조: 객체는 주소로 전달돼요', '숫자는 복사되지만 객체는 <b>같은 객체를 가리키는 주소</b>가 복사돼요. 그래서 b를 바꾸면 a도 바뀌어요. 독립된 복사본이 필요하면 <code>{...a}</code>나 <code>structuredClone(a)</code>를 써요.', 'const a = { score: 1 };\nconst b = a;        // 같은 객체\nb.score = 99;\nconsole.log(a.score);  // 99\nconst c = { ...a }; // 복사본\nc.score = 0;\nconsole.log(a.score);  // 그대로 99'),
 ], q=[
  out('const o = { x: 1, y: 2 };\nconsole.log(o.y);', ['2', '1', 'y', 'undefined']),
  out('const o = { a: 1 };\nconsole.log(o.b);', ['undefined', 'null', '에러', '0'], '없는 속성은 에러가 아니라 undefined예요.'),
  out('const o = { n: 1 };\no.n = 5;\nconsole.log(o.n);', ['5', '1', '에러(const라서)', 'undefined'], 'const는 재할당만 막고 속성 수정은 허용해요.'),
  out('const a = { v: 1 };\nconst b = a;\nb.v = 2;\nconsole.log(a.v);', ['2', '1', 'undefined', '에러'], '같은 객체를 가리켜요.'),
  out('const p = { k: "x", n: 3 };\nconsole.log(Object.keys(p).length);', ['2', '3', '1', 'undefined']),
  mc('메서드 안에서 자기 객체를 가리키는 키워드는?', ['this', 'self', 'me', 'that']),
  fill('클래스로 새 객체를 만드세요', 'class Pet {}\nconst p = ▢ Pet();', ['new', 'make', 'create', 'class']),
  fill('name만 꺼내는 구조 분해', 'const user = { name: "A", age: 3 };\nconst { ▢ } = user;', ['name', 'user', '"name"', 'name: user']),
  task('title과 page 속성을 가진 객체 book을 만들고 book.title을 출력하세요 (title은 코딩)', 'const book = { title: "코딩", page: 200 };\nconsole.log(book.title);', '', expect='코딩', need=[r'\{']),
 ]),
 dict(id='js10', t='폼과 이벤트 다루기', ic='input', d='input·select 값 읽기, change·submit 이벤트', lang='html', cards=[
  card('입력값 읽기: value', 'input과 select의 현재 값은 <code>.value</code>로 읽어요. 값은 항상 <b>문자열</b>이라 숫자로 계산하려면 <code>Number()</code>로 바꿔요. 체크박스는 <code>.checked</code>(true/false)를 봐요.', '<input id="a" type="number" value="3">\n<input id="b" type="number" value="4">\n<button id="go">더하기</button>\n<p id="out"></p>\n<script>\n  document.querySelector("#go").addEventListener("click", () => {\n    const a = Number(document.querySelector("#a").value);\n    const b = Number(document.querySelector("#b").value);\n    document.querySelector("#out").textContent = a + b;\n  });\n</script>'),
  card('셀렉트박스 값 바꾸면: change', 'select·checkbox는 값이 바뀔 때 <code>change</code> 이벤트가, 글자 입력은 한 글자마다 <code>input</code> 이벤트가 일어나요. 고른 option의 글자는 <code>selectedOptions[0].text</code>, 전송값은 <code>value</code>예요.', '<select id="s">\n  <option value="red">빨강</option>\n  <option value="blue">파랑</option>\n  <option value="green">초록</option>\n</select>\n<p id="msg">색을 고르세요</p>\n<script>\n  const s = document.querySelector("#s");\n  s.addEventListener("change", () => {\n    const msg = document.querySelector("#msg");\n    msg.textContent = s.selectedOptions[0].text + " 선택 (" + s.value + ")";\n    msg.style.color = s.value;\n  });\n</script>'),
  card('select에 option 넣기', '데이터 배열로 option을 만들 땐 <code>new Option(글자, 값)</code>이나 <code>document.createElement("option")</code>을 쓰고 <code>append</code>로 붙여요.', '<select id="fruit"></select>\n<script>\n  const list = ["사과", "배", "포도"];\n  const sel = document.querySelector("#fruit");\n  list.forEach((name, i) => sel.append(new Option(name, i)));\n</script>'),
  card('폼 제출: submit과 preventDefault', '폼은 제출하면 페이지가 새로고침돼요. JS로 처리하려면 <code>submit</code> 이벤트에서 <code>e.preventDefault()</code>로 기본 동작을 막아요. 입력 검사도 여기서 해요.', '<form id="f">\n  <input id="nick" placeholder="닉네임 (2자 이상)">\n  <button>가입</button>\n</form>\n<p id="r"></p>\n<script>\n  document.querySelector("#f").addEventListener("submit", (e) => {\n    e.preventDefault();\n    const v = document.querySelector("#nick").value.trim();\n    document.querySelector("#r").textContent = v.length >= 2 ? v + "님 환영!" : "2자 이상 입력하세요";\n  });\n</script>'),
 ], q=[
  mc('input의 현재 입력값을 읽는 속성은?', ['value', 'text', 'content', 'input']),
  mc('select에서 다른 항목을 고를 때 일어나는 이벤트는?', ['change', 'click', 'submit', 'load']),
  mc('폼 제출 시 페이지 새로고침을 막는 코드는?', ['e.preventDefault()', 'e.stop()', 'return true', 'form.cancel()']),
  mc('체크박스가 체크됐는지 알려 주는 속성은?', ['checked', 'value', 'selected', 'on']),
  out('<input id="n" value="5">\n<script>\n  const v = document.querySelector("#n").value;\n  console.log(v + 1);\n</script>', ['51', '6', 'NaN', '에러'], 'value는 문자열이라 "5" + 1 = "51"이에요.', q='콘솔에 찍히는 값은?'),
  fill('select에서 고른 값 읽기', 'const city = document.querySelector("#city").▢;', ['value', 'text', 'option', 'selected']),
  task('select#pick에 option A, B를 만들고, change 때 p#out에 고른 값을 쓰는 코드를 만드세요', '<select id="pick">\n  <option>A</option>\n  <option>B</option>\n</select>\n<p id="out"></p>\n<script>\n  const p = document.querySelector("#pick");\n  p.addEventListener("change", () => {\n    document.querySelector("#out").textContent = p.value;\n  });\n</script>', '', check='(()=>{const s=doc.querySelector("#pick");if(!s||s.options.length<2)return false;s.value=s.options[1].value;s.dispatchEvent(new Event("change"));return (doc.querySelector("#out")||{}).textContent===s.value})()', need=['change']),
 ]),
 dict(id='js11', t='JSON·저장·서버 통신', ic='fetch', d='JSON, localStorage, fetch와 async/await', cards=[
  card('JSON: 데이터를 주고받는 글자 형식', '<b>JSON</b>은 객체·배열을 문자열로 표현하는 형식이에요. 서버와 앱이 데이터를 주고받을 때 거의 항상 써요. <code>JSON.stringify(객체)</code>로 문자열로, <code>JSON.parse(문자열)</code>로 다시 객체로 바꿔요. 키는 반드시 큰따옴표로 감싸요.', 'const user = { name: "민수", tags: ["코딩", "게임"] };\nconst text = JSON.stringify(user);\nconsole.log(text);\nconst back = JSON.parse(text);\nconsole.log(back.tags[0]);'),
  card('localStorage: 브라우저에 저장', '<code>localStorage.setItem(키, 문자열)</code>로 저장하면 페이지를 닫아도 남아요. 객체는 JSON으로 바꿔 저장해요. 이 학습 앱의 진도도 이런 방식으로 저장돼요. (여기 실행기는 실제 저장소 대신 실행할 때마다 비워지는 연습용 저장소를 써요.) 단, 같은 기기·브라우저에만 있고 <b>비밀번호 같은 민감 정보는 저장하면 안 돼요</b>.', 'const data = { level: 3, xp: 120 };\nlocalStorage.setItem("save", JSON.stringify(data));\nconst loaded = JSON.parse(localStorage.getItem("save"));\nconsole.log("레벨", loaded.level);'),
  card('비동기: 기다리는 동안 멈추지 않기', '서버 응답처럼 시간이 걸리는 일은 <b>비동기</b>로 처리해요. <code>Promise</code>는 "나중에 결과를 주겠다는 약속"이고, <code>async</code> 함수 안에서 <code>await</code>로 결과를 기다려요. 기다리는 동안 화면은 멈추지 않아요.', 'function wait(ms) {\n  return new Promise(ok => setTimeout(ok, ms));\n}\nasync function run() {\n  console.log("시작");\n  await wait(500);\n  console.log("0.5초 뒤");\n}\nrun();\nconsole.log("run을 부른 다음 줄");'),
  card('fetch로 서버에서 데이터 받기', '<code>fetch(주소)</code>로 서버에 요청하고, 응답을 <code>.json()</code>으로 객체로 바꿔요. 네트워크는 실패할 수 있으니 <code>try/catch</code>로 감싸고 <code>res.ok</code>를 확인해요. 앱이 서버의 <b>API</b>와 대화하는 기본 방법이에요.', '// 실제 서버 대신 가짜 응답으로 흐름만 보여 줘요\nasync function getWeather() {\n  try {\n    const res = { ok: true, json: async () => ({ city: "서울", temp: 21 }) };\n    // 실제로는: const res = await fetch("https://api.example.com/weather");\n    if (!res.ok) throw new Error("응답 실패");\n    const data = await res.json();\n    console.log(data.city, data.temp + "도");\n  } catch (err) {\n    console.log("에러:", err.message);\n  }\n}\ngetWeather();'),
 ], q=[
  mc('객체를 JSON 문자열로 바꾸는 함수는?', ['JSON.stringify', 'JSON.parse', 'String()', 'toJSON']),
  mc('JSON 문자열을 객체로 바꾸는 함수는?', ['JSON.parse', 'JSON.stringify', 'Object()', 'eval']),
  out('const t = JSON.stringify({ a: 1 });\nconsole.log(typeof t);', ['string', 'object', 'number', 'json']),
  out('console.log("1");\nsetTimeout(() => console.log("2"), 0);\nconsole.log("3");', ['1\n3\n2', '1\n2\n3', '2\n1\n3', '3\n2\n1'], 'setTimeout은 0초여도 현재 코드가 끝난 뒤 실행돼요.'),
  mc('localStorage에 저장하면 안 되는 것은?', ['비밀번호', '화면 테마 설정', '학습 진도', '최근 본 단원']),
  fill('Promise 결과를 기다리세요', 'async function f() {\n  const data = ▢ getData();\n}', ['await', 'async', 'wait', 'then']),
  mc('fetch 요청이 실패할 때를 대비하는 방법은?', ['try/catch로 감싸고 res.ok 확인', '무조건 성공한다고 가정', 'alert만 띄운다', 'for문으로 감싼다']),
 ]),
]

SEC = [
 dict(id='sc1', t='보안의 기본 생각', ic='🔒', d='CIA, 공격 표면, 최소 권한, 입력은 믿지 않기', cards=[
  card('보안의 세 기둥: CIA', '<b>기밀성</b>(Confidentiality, 허락된 사람만 본다), <b>무결성</b>(Integrity, 몰래 바뀌지 않는다), <b>가용성</b>(Availability, 필요할 때 쓸 수 있다). 모든 보안 대책은 이 셋 중 무엇을 지키는지로 설명할 수 있어요. 비밀번호 유출은 기밀성, 성적 조작은 무결성, 디도스(DDoS)는 가용성 침해예요.'),
  card('사용자 입력은 절대 믿지 않는다', '해커는 입력칸에 이름 대신 코드를 넣어요. 브라우저의 <code>required</code>, <code>maxlength</code> 같은 검사는 개발자 도구로 쉽게 지울 수 있어요. 그래서 <b>서버에서 다시 검사</b>하고, 허용할 형식만 통과시키는(화이트리스트) 방식이 안전해요.', 'function isValidNickname(s) {\n  // 한글·영문·숫자 2~10자만 허용 (화이트리스트)\n  return /^[가-힣a-zA-Z0-9]{2,10}$/.test(s);\n}\nconsole.log(isValidNickname("민수123"));\nconsole.log(isValidNickname("<script>"));\nconsole.log(isValidNickname("a"));'),
  card('최소 권한과 심층 방어', '<b>최소 권한</b>: 각 사용자·프로그램에 꼭 필요한 권한만 줘요. 일반 회원 계정으로 관리자 기능에 접근할 수 없어야 해요. <b>심층 방어</b>: 한 겹이 뚫려도 다음 겹이 막도록 여러 층(입력 검사, 권한 확인, 암호화, 로그 감시)을 둬요.'),
  card('흔한 공격 한눈에 보기', '<b>피싱</b>: 가짜 사이트·문자로 비밀번호를 훔쳐요. <b>XSS</b>: 웹페이지에 악성 스크립트를 심어요. <b>SQL 인젝션</b>: 입력으로 데이터베이스 명령을 조작해요. <b>무차별 대입</b>: 비밀번호를 하나씩 계속 시도해요. <b>악성 패키지</b>: 이름이 비슷한 라이브러리에 악성코드를 숨겨요. 다음 단원에서 하나씩 막는 법을 배워요.'),
 ], q=[
  mc('성적이 몰래 수정되는 것은 CIA 중 무엇의 침해인가요?', ['무결성', '기밀성', '가용성', '편의성']),
  mc('서비스를 마비시키는 DDoS 공격이 침해하는 것은?', ['가용성', '기밀성', '무결성', '인증']),
  mc('브라우저의 required 검사만 믿으면 안 되는 이유는?', ['사용자가 쉽게 우회할 수 있어서', '브라우저가 느려서', '모바일에서 안 돼서', '디자인이 바뀌어서']),
  out('console.log(/^[0-9]{3}$/.test("12a"));', ['false', 'true', '12a', '에러'], '숫자 3자리만 허용하는 정규식이에요.'),
  mc('꼭 필요한 권한만 주는 원칙은?', ['최소 권한', '최대 편의', '전체 공개', '관리자 우선']),
  mc('입력 검사에서 더 안전한 방식은?', ['허용할 형식만 통과(화이트리스트)', '위험한 단어만 막기(블랙리스트)', '검사하지 않기', '길이만 확인']),
 ]),
 dict(id='sc2', t='웹 보안: XSS와 인젝션', ic='XSS', d='innerHTML의 위험, 이스케이프, SQL 인젝션, 준비된 쿼리', lang='html', cards=[
  card('XSS: 남의 페이지에 내 스크립트 심기', '게시판 글이나 닉네임에 <code>&lt;img src=x onerror=...&gt;</code> 같은 코드를 넣으면, 그 글을 보는 다른 사람의 브라우저에서 스크립트가 실행돼요. 로그인 정보를 훔치거나 화면을 바꿀 수 있어요. 원인은 <b>입력을 HTML로 그대로 넣는 것</b>이에요.'),
  card('textContent vs innerHTML', '<code>innerHTML</code>은 글자를 HTML로 해석해서 태그와 이벤트가 살아나요. <code>textContent</code>는 무조건 글자로만 보여 줘요. 사용자가 입력한 값을 화면에 보여 줄 땐 <b>textContent</b>를 쓰는 게 기본이에요.', '<p id="a"></p>\n<p id="b"></p>\n<script>\n  const evil = "<b>굵게?</b> <i>기울임?</i>";\n  document.querySelector("#a").innerHTML = evil;   // 태그가 해석됨\n  document.querySelector("#b").textContent = evil; // 글자 그대로\n</script>'),
  card('이스케이프: 특수문자를 무해하게', 'HTML 안에 꼭 넣어야 한다면 <code>&lt; &gt; &amp; " \'</code>를 <code>&amp;lt;</code> 같은 엔티티로 바꿔(이스케이프) 넣어요. React·Vue 같은 프레임워크는 기본으로 이스케이프해 줘요. 여기에 <b>CSP</b>(콘텐츠 보안 정책) 헤더를 더하면 허락하지 않은 스크립트 실행을 막을 수 있어요.', '<p id="out"></p>\n<script>\n  function esc(s) {\n    return s.replace(/[&<>"\']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",\'"\':"&quot;","\'":"&#39;"}[c]));\n  }\n  const input = "<script>alert(1)<\\/script>";\n  document.querySelector("#out").innerHTML = "입력: " + esc(input);\n</script>'),
  card('SQL 인젝션', '로그인을 <code>"SELECT * FROM users WHERE id=\'" + 입력 + "\'"</code>처럼 문자열로 이어 만들면, 입력에 <code>\' OR \'1\'=\'1</code>을 넣는 순간 조건이 항상 참이 돼 비밀번호 없이 로그인돼요. 해결책은 <b>준비된 쿼리</b>(prepared statement, 매개변수 바인딩)예요. 입력은 데이터로만 취급되고 명령으로 해석되지 않아요.', '<pre id="q"></pre>\n<script>\n  const input = "\' OR \'1\'=\'1";\n  const bad = "SELECT * FROM users WHERE id=\'" + input + "\'";\n  const good = "SELECT * FROM users WHERE id = ?   -- 값: " + JSON.stringify(input);\n  document.querySelector("#q").textContent = "위험: " + bad + "\\n안전: " + good;\n</script>'),
 ], q=[
  mc('사용자 입력을 화면에 보여 줄 때 더 안전한 속성은?', ['textContent', 'innerHTML', 'outerHTML', 'document.write']),
  mc('SQL 인젝션을 막는 가장 확실한 방법은?', ['준비된 쿼리(매개변수 바인딩)', '입력 길이 제한만', '비밀번호 복잡하게', 'HTTPS 사용']),
  mc('XSS 공격의 근본 원인은?', ['사용자 입력을 HTML로 그대로 넣는 것', '비밀번호가 짧은 것', '서버가 느린 것', '이미지가 큰 것']),
  out('<p id="p"></p>\n<script>\n  document.querySelector("#p").textContent = "<b>hi</b>";\n</script>', ['<b>hi</b> (글자 그대로)', 'hi (굵게)', '아무것도 안 보임', '에러'], '', q='화면에 보이는 것은?'),
  mc('"<"를 HTML 엔티티로 바꾸면?', ['&lt;', '&gt;', '&amp;', '&quot;']),
  bug('<p id="name"></p>\n<script>\n  const nick = prompt("닉네임");\n  document.querySelector("#name").innerHTML = nick;\n</script>', 3, '사용자 입력을 innerHTML에 넣으면 XSS 위험이 있어요. textContent를 쓰세요.', q='보안상 위험한 줄은?'),
 ]),
 dict(id='sc3', t='비밀번호와 인증', ic='🔑', d='해시와 솔트, 2단계 인증, 세션·토큰', cards=[
  card('비밀번호는 저장하지 않는다', '서버는 비밀번호 원문을 저장하면 안 돼요. 대신 되돌릴 수 없는 <b>해시</b>(비밀번호 → 고정 길이의 지문)를 저장하고, 로그인 때 입력값을 같은 방식으로 해시해 비교해요. 해커가 DB를 훔쳐도 원문을 바로 알 수 없어요.'),
  card('솔트와 느린 해시', '같은 비밀번호는 같은 해시가 나와서, 미리 계산한 표(레인보우 테이블)로 역추적될 수 있어요. 사용자마다 다른 무작위 값 <b>솔트</b>를 붙여 해시하면 이를 막아요. 또 비밀번호용으로는 일부러 느리게 설계된 <b>bcrypt, scrypt, Argon2</b>를 써요. 빠른 해시(MD5, SHA-1)는 무차별 대입에 약해요.', '// 브라우저 내장 암호 기능으로 SHA-256 해시 보기 (학습용)\nasync function sha256(text) {\n  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));\n  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, "0")).join("");\n}\n(async () => {\n  console.log(await sha256("password123"));\n  console.log(await sha256("password124")); // 한 글자만 달라도 완전히 다름\n})();'),
  card('좋은 비밀번호와 2단계 인증', '길이가 가장 중요해요. 짧고 복잡한 것보다 <b>긴 문장형</b>이 강해요. 사이트마다 다른 비밀번호를 쓰고 <b>비밀번호 관리자</b>를 활용해요. 그리고 <b>2단계 인증(2FA)</b>을 켜면 비밀번호가 유출돼도 인증 앱·보안키 없이는 로그인할 수 없어요. 문자(SMS) 인증보다 인증 앱이나 패스키가 더 안전해요.'),
  card('세션과 토큰', '로그인에 성공하면 서버는 "이 사람은 인증됨"을 기억할 표식(세션 ID 쿠키나 JWT 토큰)을 줘요. 이 표식을 훔치면 비밀번호 없이도 로그인한 척할 수 있어요. 그래서 쿠키에 <code>HttpOnly</code>(JS로 못 읽음), <code>Secure</code>(HTTPS로만), <code>SameSite</code>(다른 사이트 요청에 안 붙음)를 설정하고, 토큰은 만료 시간을 짧게 둬요.'),
 ], q=[
  mc('서버가 비밀번호를 저장하는 올바른 방법은?', ['솔트를 붙여 느린 해시로 저장', '원문 그대로 저장', '앞 세 글자만 저장', 'Base64로 인코딩해 저장']),
  mc('비밀번호 저장용으로 적합한 알고리즘은?', ['bcrypt·Argon2', 'MD5', 'Base64', 'ROT13']),
  mc('사용자마다 다른 무작위 값을 붙여 해시하는 이유는?', ['미리 계산된 해시표(레인보우 테이블) 공격을 막으려고', '로그인을 빠르게 하려고', '비밀번호를 짧게 하려고', '서버 용량을 줄이려고']),
  mc('비밀번호가 유출돼도 계정을 지켜 주는 것은?', ['2단계 인증', '자동 로그인', '비밀번호 힌트', '같은 비밀번호 재사용']),
  mc('JavaScript가 쿠키를 읽지 못하게 막는 쿠키 속성은?', ['HttpOnly', 'Secure', 'Path', 'Expires']),
  mc('더 강한 비밀번호는?', ['purple-tiger-eats-7-noodles', 'P@ss1', 'qwerty123', '19990101']),
 ]),
 dict(id='sc4', t='개인정보·HTTPS·비밀키 관리', ic='🛡', d='HTTPS, API 키 숨기기, 의존성, 개인정보 최소 수집', cards=[
  card('HTTPS', 'HTTP는 데이터를 평문으로 보내서 같은 와이파이의 누군가가 엿볼 수 있어요. <b>HTTPS</b>는 TLS로 암호화하고, 인증서로 "진짜 그 사이트"인지 확인해요. 로그인·결제가 있는 사이트는 물론 모든 사이트가 HTTPS를 쓰는 게 기본이에요.'),
  card('API 키는 코드에 넣지 않는다', '깃허브 공개 저장소에 API 키·비밀번호를 올리면 몇 분 안에 자동 수집 봇이 가져가요. 비밀 값은 <b>환경 변수</b>나 비밀 관리 서비스에 두고, <code>.gitignore</code>로 설정 파일을 제외해요. 또 프론트엔드(브라우저·앱) 코드에 들어간 키는 누구나 볼 수 있으니, 비밀 키가 필요한 요청은 <b>서버를 거쳐서</b> 해요.', '// 나쁜 예: 앱 코드에 비밀 키 직접 작성\n// const KEY = "sk-live-12345...";\n\n// 좋은 예(서버): 환경 변수에서 읽기\n// const KEY = process.env.PAYMENT_KEY;\nconsole.log("비밀 키는 서버의 환경 변수에!");'),
  card('남이 만든 코드도 위험할 수 있다', '앱은 수백 개의 라이브러리(의존성)에 기대요. 오래된 버전엔 알려진 취약점이 있고, 이름이 비슷한 가짜 패키지(타이포스쿼팅)도 있어요. <code>npm audit</code> 같은 도구로 취약점을 점검하고, 유명하고 관리되는 패키지만 써요.'),
  card('개인정보는 적게, 짧게', '필요 없는 개인정보는 <b>처음부터 수집하지 않는 것</b>이 최고의 보안이에요. 주민등록번호·위치·연락처는 꼭 필요할 때만 받고, 목적이 끝나면 지워요. 한국은 개인정보보호법으로 수집 동의, 보관 기간, 유출 신고를 의무화하고 있어요. 앱 권한(카메라·위치)도 필요한 순간에만 요청해요.'),
  card('실제 사고에서 배우기', '2014년 하트블리드(OpenSSL 버그)는 수많은 서버의 메모리를 엿볼 수 있게 했어요. 2017년 에퀴팩스는 패치 안 한 웹 프레임워크 취약점으로 약 1억 4천만 명의 개인정보가 유출됐어요. 2021년 Log4Shell은 로그 라이브러리 하나로 전 세계 서버가 위험해졌어요. 공통 교훈은 <b>업데이트를 미루지 말 것</b>이에요.'),
 ], q=[
  mc('HTTPS가 해 주는 일은?', ['통신 암호화와 사이트 신원 확인', '사이트 속도 2배', '광고 차단', '비밀번호 자동 생성']),
  mc('API 비밀 키를 보관하기에 알맞은 곳은?', ['서버의 환경 변수', '공개 깃허브 코드', '앱의 JavaScript 파일', '웹페이지 주석']),
  mc('에퀴팩스 유출 사고의 주된 원인은?', ['알려진 취약점을 패치하지 않음', '직원이 비밀번호를 공유함', '전기가 끊김', 'HTTPS를 너무 많이 씀']),
  mc('개인정보 보호의 가장 좋은 출발점은?', ['필요 없는 정보는 아예 수집하지 않기', '모든 정보를 수집해 두기', '암호화만 하면 무엇이든 저장', '사용자에게 알리지 않기']),
  mc('설정 파일을 Git에 올리지 않도록 제외하는 파일은?', ['.gitignore', 'README.md', 'package.json', 'index.html']),
  mc('의존성 취약점을 점검하는 명령의 예는?', ['npm audit', 'npm start', 'git push', 'ls -al']),
 ]),
]

APP = [
 dict(id='ap1', t='앱은 어떻게 이루어지나', ic='📱', d='프론트엔드·백엔드·API·데이터베이스', cards=[
  card('세 부분: 화면, 서버, 저장소', '<b>프론트엔드</b>는 사용자가 보는 화면(HTML·CSS·JS, 안드로이드·iOS 화면)이에요. <b>백엔드</b>는 서버에서 로그인 확인, 결제, 데이터 처리를 해요(Python, Node.js, Java 등). <b>데이터베이스</b>는 회원·게시글 같은 데이터를 저장해요(MySQL, PostgreSQL, Firebase 등).'),
  card('API: 화면과 서버의 약속', '프론트엔드는 서버에 "요청"을 보내고 서버는 JSON으로 "응답"해요. 이 주소와 형식의 약속이 <b>API</b>예요. REST API는 주소(/users/3)와 동작(GET 읽기, POST 만들기, PUT·PATCH 수정, DELETE 삭제)으로 표현해요. 응답 코드 200은 성공, 404는 없음, 500은 서버 오류예요.', '// 요청과 응답의 모양 (예시)\nconst request = { method: "GET", url: "/api/users/3" };\nconst response = { status: 200, body: { id: 3, name: "민수" } };\nconsole.log(request.method, request.url, "→", response.status, response.body.name);'),
  card('앱의 종류', '<b>웹앱</b>: 브라우저에서 바로 실행, 설치 불필요. <b>네이티브 앱</b>: 안드로이드(Kotlin)·iOS(Swift)로 각각 개발, 성능·기기 기능 최고. <b>크로스플랫폼</b>: 한 코드로 둘 다(Flutter, React Native). <b>하이브리드</b>: 웹 코드를 앱 껍데기에 넣음(Capacitor). 지금 쓰고 있는 이 학습 앱이 바로 HTML·JS로 만들고 Capacitor로 안드로이드 앱이 된 하이브리드 앱이에요.'),
  card('기획부터 출시까지', '① 문제 정의(누가, 왜 쓰나) ② 화면 설계(와이어프레임) ③ 데이터 설계(무엇을 저장하나) ④ 개발 ⑤ 테스트 ⑥ 배포 ⑦ 사용자 반응 보고 개선. 처음부터 다 만들지 말고 핵심 기능 하나만 있는 <b>MVP</b>(최소 기능 제품)로 빨리 내보고 고쳐요.'),
 ], q=[
  mc('사용자가 보고 만지는 화면 부분은?', ['프론트엔드', '백엔드', '데이터베이스', '운영체제']),
  mc('REST API에서 새 데이터를 만들 때 주로 쓰는 메서드는?', ['POST', 'GET', 'DELETE', 'HEAD']),
  mc('HTTP 응답 코드 404의 뜻은?', ['찾을 수 없음', '성공', '서버 오류', '권한 있음']),
  mc('한 코드로 안드로이드와 iOS 앱을 함께 만드는 도구는?', ['Flutter', 'Excel', 'Photoshop', 'MySQL']),
  mc('핵심 기능만 담아 빠르게 출시하는 첫 버전을 뭐라고 하나요?', ['MVP', 'API', 'SQL', 'CSS']),
  out('const res = { status: 200, body: { ok: true } };\nconsole.log(res.status === 200 ? "성공" : "실패");', ['성공', '실패', '200', 'true']),
 ]),
 dict(id='ap2', t='작은 앱 직접 만들기', ic='✅', d='할 일 앱: 상태, 화면 그리기, 저장', lang='html', cards=[
  card('상태(state)와 화면 그리기', '앱의 핵심 패턴은 <b>데이터(상태)를 바꾸고 → 화면을 다시 그린다</b>예요. 화면을 직접 이리저리 고치지 말고, 배열 같은 상태만 바꾼 뒤 <code>render()</code> 함수로 전체를 다시 그리면 버그가 줄어요. React·Vue 같은 프레임워크가 이 아이디어를 자동화해요.', '<input id="t" placeholder="할 일">\n<button id="add">추가</button>\n<ul id="list"></ul>\n<script>\n  let todos = [{ text: "코딩 30분", done: false }];\n  function render() {\n    const ul = document.querySelector("#list");\n    ul.innerHTML = "";\n    todos.forEach((td, i) => {\n      const li = document.createElement("li");\n      li.textContent = (td.done ? "✔ " : "□ ") + td.text;\n      li.onclick = () => { todos[i].done = !todos[i].done; render(); };\n      ul.append(li);\n    });\n  }\n  document.querySelector("#add").onclick = () => {\n    const v = document.querySelector("#t").value.trim();\n    if (v) { todos.push({ text: v, done: false }); render(); }\n  };\n  render();\n</script>'),
  card('저장해서 다시 열어도 남게', '상태가 바뀔 때마다 localStorage에 JSON으로 저장하고, 시작할 때 불러오면 앱을 닫아도 할 일이 남아요. 실제 서비스라면 이 자리에 서버 API 호출이 들어가요.', '<p id="c"></p>\n<button id="b">+1</button>\n<script>\n  let count = Number(localStorage.getItem("cnt") || 0);\n  const show = () => document.querySelector("#c").textContent = "누른 횟수: " + count;\n  document.querySelector("#b").onclick = () => {\n    count++;\n    localStorage.setItem("cnt", count);\n    show();\n  };\n  show();\n</script>'),
  card('컴포넌트로 나누기', '화면을 재사용 가능한 조각(<b>컴포넌트</b>)으로 나눠요. "할 일 하나"를 그리는 함수를 만들고 여러 번 쓰는 식이에요. 앱이 커질수록 컴포넌트와 상태 관리가 중요해져요.', '<div id="app"></div>\n<script>\n  function Card(title, body) {\n    const el = document.createElement("div");\n    el.style.cssText = "border:1px solid #ccc;border-radius:10px;padding:8px;margin:6px 0";\n    const h = document.createElement("b");\n    h.textContent = title;\n    const p = document.createElement("p");\n    p.textContent = body;\n    el.append(h, p);\n    return el;\n  }\n  const app = document.querySelector("#app");\n  app.append(Card("오늘의 목표", "단원 1개 끝내기"), Card("복습", "틀린 문제 다시 보기"));\n</script>'),
 ], q=[
  mc('앱의 핵심 패턴으로 알맞은 것은?', ['상태를 바꾸고 화면을 다시 그린다', '화면을 그때그때 직접 고친다', '데이터는 저장하지 않는다', '모든 코드를 한 줄에 쓴다']),
  mc('앱을 닫아도 데이터가 남게 하는 브라우저 저장소는?', ['localStorage', 'console', 'sessionStorage만', 'alert']),
  mc('화면을 재사용 가능한 조각으로 나눈 것을 뭐라고 하나요?', ['컴포넌트', '컴파일러', '쿠키', '포트']),
  fill('배열 todos에 새 할 일을 추가하세요', 'todos.▢({ text: v, done: false });', ['push', 'add', 'append', 'insert']),
  bug('<ul id="l"></ul>\n<script>\n  const items = ["A", "B"];\n  items.forEach(x => {\n    const li = document.createElement("li");\n    li.textContent = x;\n  });\n</script>', 5, '만든 li를 ul에 붙이지 않았어요. document.querySelector("#l").append(li)가 필요해요.', q='목록이 화면에 안 보여요. 빠진 작업이 있어야 할 곳은?'),
 ]),
 dict(id='ap3', t='앱 출시와 운영', ic='🚀', d='Git, 빌드·배포, 스토어, 업데이트와 모니터링', cards=[
  card('Git: 코드의 타임머신', '<b>Git</b>은 코드 변경 이력을 저장해요. <code>commit</code>으로 저장점을 만들고, <code>branch</code>로 실험하고, <code>push</code>로 GitHub에 올려요. 실수해도 이전 버전으로 돌아갈 수 있고, 여러 명이 동시에 작업할 수 있어요.', '// 터미널에서 쓰는 기본 흐름\nconst steps = [\n  "git add .",\n  "git commit -m \\"할 일 추가 기능\\"",\n  "git push origin main",\n];\nsteps.forEach(s => console.log("$ " + s));'),
  card('빌드와 자동 배포(CI/CD)', '코드를 올리면 자동으로 테스트하고 앱 파일(APK·AAB)이나 웹사이트를 만들어 배포하는 과정을 <b>CI/CD</b>라고 해요. 이 학습 앱도 GitHub에 코드를 올리면 GitHub Actions가 자동으로 안드로이드 앱을 빌드하고 웹사이트를 갱신해요.'),
  card('앱 서명과 스토어', '안드로이드 앱은 개발자의 <b>서명 키</b>로 서명돼요. 업데이트는 같은 키로 서명해야 설치되고, 키를 잃어버리면 업데이트를 못 해요. 플레이스토어에 올리려면 개발자 계정, 개인정보처리방침, 앱 설명·스크린샷, 콘텐츠 등급, 테스트 기간이 필요해요. 스토어 앱은 구글의 보안 검사를 거쳐요.'),
  card('버전과 업데이트', '버전은 보통 <b>주.부.수</b>(1.4.2) 형식으로 써요. 큰 변화는 주, 기능 추가는 부, 버그 수정은 수 번호를 올려요. 안드로이드는 별도로 숫자 versionCode가 계속 커져야 업데이트가 돼요. 출시 후에는 크래시 리포트, 사용자 리뷰, 사용 통계를 보고 개선해요.'),
  card('웹앱도 앱처럼: PWA', '<b>PWA</b>(프로그레시브 웹앱)는 웹사이트에 매니페스트와 서비스 워커를 더해 홈 화면에 설치하고 오프라인에서도 동작하게 해요. 이 학습 앱의 웹 버전도 PWA라서 인터넷 없이도 열려요.'),
 ], q=[
  mc('코드 변경 이력을 저장하고 되돌릴 수 있게 하는 도구는?', ['Git', 'Excel', 'Chrome', 'Figma']),
  mc('변경 사항을 저장점으로 기록하는 Git 명령은?', ['commit', 'push', 'clone', 'status']),
  mc('코드를 올리면 자동으로 테스트·빌드·배포하는 것을 뭐라고 하나요?', ['CI/CD', 'DNS', 'SQL', 'CSS']),
  mc('안드로이드 앱 업데이트가 설치되려면?', ['이전과 같은 서명 키로 서명', '앱 이름을 바꾸기', '아이콘을 바꾸기', '용량을 줄이기']),
  mc('버전 1.4.2에서 버그만 고쳤다면 다음 버전은?', ['1.4.3', '2.0.0', '1.5.0', '1.4.2']),
  mc('웹사이트를 홈 화면에 설치하고 오프라인에서도 쓰게 하는 기술은?', ['PWA', 'FTP', 'SSH', 'VPN']),
 ]),
]
