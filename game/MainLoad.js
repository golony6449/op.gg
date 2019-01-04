// Main Image Load 부분 //

/* 
image 첩자 확인 

0 : 메인화면 이미지
1 : 메인화면 제목
2 ~ 7 : 버튼

*/

// 게임의 상태 //
var PROCESS_Main = 0;
var PROCESS_Start = 1;
var PROCESS_Help = 2;
var PROCESS_Producer = 3;
var PROCESS_End = 4;
var state = PROCESS_Main;


// 메인 0 , 게임플레이 1, 방법창 2 제작자창 3 게임 엔딩 4

var canvas;
var ctx;
var loadcount = 0;
var Count = 5; // 몇 개의 이미지를 만들지 카운터 객수 배열보다 하나 더 0부터 시작해서..
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
	
	img[EffectMotion.SpriteImage].src="Image/Main/메인화면.png";		// 메인 화면 이미지
	img[1].src="Image/Main/제목.png";			 // 메인 화면 제목
	img[2].src="Image/Main/help.png";	
	img[3].src="Image/Main/help.png";
	img[4].src="Image/Start/맵.jpg";
	
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
	switch ( state )
		{
			case PROCESS_Main: // 메인 화면 관리 프로세스 0
				drawMain();
				break;
			case PROCESS_Start: // 게임 시작 관리 프로세스 1
				
				location.href="start.html";
				break;
			case PROCESS_Help: // 게임 방법 관리 프로세스 2
				ctx.drawImage(img[2],0,0);
				
				break;
			case PROCESS_Producer: // 게임 제작자 관리 프로세스 3 
				ctx.drawImage(img[3],0,0);
				
				break;
			case PROCESS_End: // 게임 엔딩 관리 프로세스4
				
				break;
			
		}
	
}

function drawMain() 
{

	if (loadcount != Count)
	{
		ctx.font="30px arial";
		ctx.fillText("로딩중...", 100, 100);
	}else if ( state == PROCESS_Start) {
		ctx.drawImage(img[4],0,0);
	} else {
		if ( EffectMotion.SpriteMin < 68 ) // 잘했어요 이펙트
		{	
			EffectMotion.SpriteCount ++ ;
			ctx.drawImage(img[EffectMotion.SpriteImage], EffectMotion.SpriteMin % 10 * 800, Math.floor(EffectMotion.SpriteMin / 10 ) * 480,
				   	800, 480, EffectMotion.x, EffectMotion.y, 800, 480);
			if ( EffectMotion.SpriteCount > 3 )
			{
					// console.log(EffectMotion.SpriteMin);
					EffectMotion.SpriteMin = (EffectMotion.SpriteMin +1) % EffectMotion.SpriteMax;
					EffectMotion.SpriteCount = 0;
			}
		}else{
			EffectMotion.SpriteMin = 0;
			ctx.drawImage(img[EffectMotion.SpriteImage], EffectMotion.SpriteMin % 10 * 800, Math.floor(EffectMotion.SpriteMin / 10 ) * 480,
				   	800, 480, EffectMotion.x, EffectMotion.y, 800, 480);
		}
		
		ctx.drawImage(img[1], 0, 0); // 제목

	}
}
function Main_Strat()
{
	state = PROCESS_Start;
	GameProcess();
}

function Main_Magyarazat()
{
	state = PROCESS_Help;
	GameProcess();
}
function Main_Producer()
{
	state = PROCESS_Producer;
	GameProcess();
}


























































