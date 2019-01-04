// Main Image Load 부분 //

/* 
image 첩자 확인 

0 : 메인화면 이미지
1 : 메인화면 제목
2 ~ 7 : 버튼

*/


// 메인 0 , 게임플레이 1, 방법창 2 제작자창 3 게임 엔딩 4

var canvas;
var ctx;
var loadcount = 0;
var Count = 1; // 몇 개의 이미지를 만들지 카운터 객수 배열보다 하나 더 0부터 시작해서..
var img = new Array(Count);

var x = 100;
var y = 100;


var EffectMotion = {}; 
EffectMotion.SpriteImage = 0, EffectMotion.SpriteMin = 0, EffectMotion.SpriteMax = 79, EffectMotion.SpriteCount = 0,
EffectMotion.x = 0 , EffectMotion.y = 0 ;


window.onload = function() 
{
	canvas = document.getElementById("canvas");

	if (canvas == null || canvas.getContext == null) return;

	ctx = canvas.getContext("2d");
	
	canvas.onmousedown = drawMain;
	GameProcess();
	
	// 이미지 객수 만큼 돌려주기 현재  조건은 임이로 정함.
	for ( var i = 0 ; i < Count ; i ++ )
	{
		img[i] = new Image(); 		// 이미지 객체 생성
		img[i].onload = function()  // 이미지 객수 카운터
		{
			loadcount++; // 증가
		}
		
	}
	
	img[EffectMotion.SpriteImage].src = "Image/Op/오프닝.png"; // 오프닝 스프라이트

	
	var timer = setInterval(function() {
		if (loadcount == Count) 
		{
			clearInterval(timer);
			 GameProcess();
		}	}, 100);
		
	setInterval(GameProcess,30);
	
}

// 돌아가는 시스템 관리 하는 부부분
function GameProcess()
{
	drawMain();
	KeyMove();
}
// 모든 키보드 처리 부분.
function KeyMove()
{
	// 키를 눌렸을 경우
	window.onkeydown = function(e) 
	{
		switch(e.keyCode) 
		{ // 플레이어 움직이는 부분 조절
			case 32:
					location.href="main.html";
				break;
	
		}
	}
}

function drawMain() 
{

	if (loadcount != Count)
	{
		ctx.font="30px arial";
		ctx.fillText("로딩중...", 100, 100);
	}else {
	
		
		
		if ( EffectMotion.SpriteMin < 78 ) // 잘했어요 이펙트
		{	
			EffectMotion.SpriteCount ++ ;
			ctx.drawImage(img[EffectMotion.SpriteImage], EffectMotion.SpriteMin % 10 * 800, Math.floor(EffectMotion.SpriteMin / 10 ) * 480,
				   	800, 480, EffectMotion.x, EffectMotion.y, 800, 480);
			if ( EffectMotion.SpriteCount > 1 )
			{
					// console.log(EffectMotion.SpriteMin);
					EffectMotion.SpriteMin = (EffectMotion.SpriteMin +1) % EffectMotion.SpriteMax;
					EffectMotion.SpriteCount = 0;
			}
		}else{
			EffectMotion.SpriteMin = 78;
			ctx.drawImage(img[EffectMotion.SpriteImage], EffectMotion.SpriteMin % 10 * 800, Math.floor(EffectMotion.SpriteMin / 10 ) * 480,
				   	800, 480, EffectMotion.x, EffectMotion.y, 800, 480);
		}

	}
}

























































