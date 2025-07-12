<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>삼각함수 애니메이션 도우미</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');

    body {
      font-family: 'Gowun Dodum', sans-serif;
      text-align: center;
      background: linear-gradient(to bottom, #f0f8ff, #e6f7ff);
      margin: 0;
      padding: 20px;
      color: #333;
    }
    h1 {
      font-size: 2em;
      margin-bottom: 20px;
      color: #004d99;
    }
    label {
      font-size: 1.1em;
      margin-bottom: 10px;
      display: block;
    }
    input[type="range"] {
      width: 60%;
      margin-bottom: 20px;
    }
    canvas {
      margin: 20px auto;
      display: block;
      border: 1px solid #ccc;
      border-radius: 10px;
      background-color: #ffffff;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .info {
      margin-top: 20px;
      font-size: 1.2em;
      background: #ffffff;
      display: inline-block;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .quiz {
      margin-top: 30px;
      background: #ffffff;
      display: inline-block;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    button {
      padding: 10px 20px;
      font-size: 1em;
      background-color: #007acc;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      margin: 5px;
      transition: background-color 0.3s;
    }
    button:hover {
      background-color: #005fa3;
    }
    input[type="text"] {
      padding: 8px;
      font-size: 1em;
      width: 200px;
      margin-top: 10px;
      margin-bottom: 10px;
      border: 1px solid #ccc;
      border-radius: 6px;
    }
    #quizResult {
      font-weight: bold;
      margin-top: 10px;
    }
  </style>
</head>
<body>
  <h1>📐 삼각함수 애니메이션 도우미</h1>

  <label for="angleSlider">각도 (&theta;): <span id="angleValue">0</span>&deg;</label>
  <input type="range" id="angleSlider" min="0" max="360" value="0">

  <canvas id="unitCircle" width="300" height="300"></canvas>
  <div class="info">
    <p>🔹 sin(&theta;) = <span id="sinValue"></span></p>
    <p>🔹 cos(&theta;) = <span id="cosValue"></span></p>
    <p>🔹 tan(&theta;) = <span id="tanValue"></span></p>
  </div>

  <canvas id="graphCanvas" width="600" height="250"></canvas>
  <div class="info">
    <p><strong>함수:</strong> <span id="functionName">y = sin(θ)</span></p>
    <p>주기: <strong>360&deg;</strong> / 진폭: <strong>1</strong> / 최대: <strong>1</strong> / 최소: <strong>-1</strong></p>
  </div>

  <div class="quiz">
    <h2>🧠 퀴즈 시간!</h2>
    <button onclick="startQuiz()">퀴즈 시작</button>
    <div id="quizQuestion"></div>
    <input type="text" id="quizAnswer" placeholder="답을 입력하세요">
    <br>
    <button onclick="checkAnswer()">제출</button>
    <div id="quizResult"></div>
  </div>

  <script>
    const angleSlider = document.getElementById("angleSlider");
    const angleValue = document.getElementById("angleValue");
    const sinValue = document.getElementById("sinValue");
    const cosValue = document.getElementById("cosValue");
    const tanValue = document.getElementById("tanValue");
    const unitCtx = document.getElementById("unitCircle").getContext("2d");

    const radius = 100;
    const centerX = 150;
    const centerY = 150;

    function drawUnitCircle(theta) {
      unitCtx.clearRect(0, 0, 300, 300);
      unitCtx.beginPath();
      unitCtx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
      unitCtx.stroke();

      const rad = theta * Math.PI / 180;
      const x = centerX + radius * Math.cos(rad);
      const y = centerY - radius * Math.sin(rad);

      unitCtx.beginPath();
      unitCtx.moveTo(centerX, centerY);
      unitCtx.lineTo(x, y);
      unitCtx.strokeStyle = 'red';
      unitCtx.stroke();

      unitCtx.beginPath();
      unitCtx.arc(x, y, 5, 0, 2 * Math.PI);
      unitCtx.fillStyle = 'blue';
      unitCtx.fill();

      sinValue.textContent = Math.sin(rad).toFixed(2);
      cosValue.textContent = Math.cos(rad).toFixed(2);
      tanValue.textContent = (Math.abs(Math.cos(rad)) < 0.0001) ? '무한' : Math.tan(rad).toFixed(2);
    }

    let graph;
    function drawGraph() {
      const labels = Array.from({ length: 361 }, (_, i) => i);
      const data = labels.map(deg => Math.sin(deg * Math.PI / 180));

      const ctx = document.getElementById("graphCanvas").getContext("2d");
      graph = new Chart(ctx, {
        type: "line",
        data: {
          labels: labels,
          datasets: [{
            label: "y = sin(θ)",
            data: data,
            borderColor: "#007acc",
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.3,
          }]
        },
        options: {
          responsive: true,
          scales: {
            x: { title: { display: true, text: "θ (deg)" } },
            y: { min: -1.2, max: 1.2, title: { display: true, text: "y" } }
          }
        }
      });
    }

    angleSlider.addEventListener("input", () => {
      const angle = parseInt(angleSlider.value);
      angleValue.textContent = angle;
      drawUnitCircle(angle);
    });

    drawUnitCircle(0);
    drawGraph();

    // 퀴즈
    const quizQuestion = document.getElementById("quizQuestion");
    const quizAnswer = document.getElementById("quizAnswer");
    const quizResult = document.getElementById("quizResult");

    let currentQuiz = {};

    function startQuiz() {
      const quizTypes = [
        { q: "y = 2sin(θ)의 진폭은?", a: "2" },
        { q: "y = cos(θ)의 주기는? (단위: 도)", a: "360" },
        { q: "y = -3sin(θ)의 최소값은?", a: "-3" },
        { q: "y = 0.5cos(θ)의 최대값은?", a: "0.5" },
      ];
      currentQuiz = quizTypes[Math.floor(Math.random() * quizTypes.length)];
      quizQuestion.textContent = currentQuiz.q;
      quizAnswer.value = "";
      quizResult.textContent = "";
    }

    function checkAnswer() {
      const userAns = quizAnswer.value.trim();
      if (userAns === currentQuiz.a) {
        quizResult.textContent = "✅ 정답입니다!";
        quizResult.style.color = "green";
      } else {
        quizResult.textContent = `❌ 오답입니다. 정답은 ${currentQuiz.a}입니다.`;
        quizResult.style.color = "red";
      }
    }
  </script>
</body>
</html>
