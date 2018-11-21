
// 게임의 상태 //
var PROCESS_Main = 0;
var PROCESS_Start_1 = 1;
var PROCESS_Start_2 = 2;
var PROCESS_Start_3 = 3;
var PROCESS_Start_4 = 4;
var PROCESS_End = 5;
var state = PROCESS_Main;


// 메인 0 , 게임플레이 1, 방법창 2 제작자창 3 게임 엔딩 4

var canvas;
var ctx;
var loadcount = 0;
var Count = 15; // 몇 개의 이미지를 만들지 카운터 객수 배열보다 하나 더 0부터 시작해서..
var img = new Array(Count);

var Mapx ; // 맵 x 값
var Mapy ; // 맵 y 값

// 사용자 캐릭터
var User={};
User.x = 75; //  사용자 x
User.y = 350; //  사용자 y

var UserBullet = new Array();
var BulletSpeed = 5;
var BulletCount = 1;
UserBulletCrate();

var arMete = new Array(); // 운석
var NUM = 5;			  // 운석 객수

var Start_2 = true;

var UserEffect = {}; 
UserEffect.SpriteImage = 13, UserEffect.SpriteMin = 0, UserEffect.SpriteMax = 101, UserEffect.SpriteCount = 0,
UserEffect.x = -500, UserEffect.y = 0;

var arMeteEffect =  new Array(); 


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
	
	img[0].src = "Image/Start/맵.jpg";			// 메인 화면 이미지
	img[1].src = img[0].src;					// 같은 메인 화면 이미지
	img[2].src = "Image/Start/캐릭터/기본.png"; // 기본 캐릭터
	img[3].src = "Image/Start/캐릭터/왼캐릭터.png"; 
	img[4].src = "Image/Start/캐릭터/기본.png"; // 캐릭터 정면
	img[5].src = "Image/Start/캐릭터/업.png"; //   캐릭터 위
	img[6].src = "Image/Start/캐릭터/다운.png"; // 캐릭터 아래
	img[7].src = "Image/Start/운석/기본.png";
	img[8].src = "Image/Start/운석/메테오.png";
	img[9].src = "Image/Start/운석/얼음.png";
	img[10].src = "Image/Start/운석/요상한.png";
	img[11].src = "Image/Start/운석/클립토나이트.png ";
	img[12].src = "Image/Start/총알/유저.png";
	img[UserEffect.SpriteImage].src = "Image/Start/이펙트/유저 부스터.png";
	img[14].src = "Image/Start/이펙트/운석 폭발.png";
	
	var timer = setInterval(function() 
	{
		if (loadcount == Count) 
		{
			clearInterval(timer);
			 GameProcess();
		}	}, 100);
	
	Mapx  = canvas.width /2;
	Mapy= canvas.height/2;
	sx = canvas.width/2;
	sy = canvas.height/2;
	
	setInterval(GameProcess,30);
	

}

// 돌아가는 시스템 관리 하는 부부분
function GameProcess()
{
	switch ( state )
		{
			case PROCESS_Main: // 메인 화면 관리 프로세스 0
				Mete(); // 운석 생성
				state = PROCESS_Start_1;
				break;
				
			case PROCESS_Start_1: // 게임 시작 관리 프로세스 1
				drawMain(); // 이미지 Darw 부분
				GameMap(); // 메인 맵 부분
				MeteStruct(); // 운석 셋팅
				
				UserBulletMove(); // 유저 총알
				
				KeyMove(); // 플레이어 움직이는 부분
				
				break;
				
			case PROCESS_Start_2: // 스테지지 2
				drawMain(); // 이미지 Darw 부분
				GameMap(); // 메인 맵 부분
				MeteStruct(); // 운석 셋팅
				Start_2_Seting();
				
				
				//UserBulletMove(); // 유저 총알
				
				KeyMove(); // 플레이어 움직이는 부분
				break;
				
			case PROCESS_Start_3: // 스테이지 3
				
				break;
				
			case PROCESS_Start_4: // 스테이지 4
				
				break;
				
			case PROCESS_End: // 게임 엔딩 관리 프로세스4
				
				break;
			
		}
	
	
}

function GameMap()
{
	// 게임 플레이 화면 맵을 2개 생성하면 무한적으로 움직이게 하기!
	if ( Mapx > -1242  )
		Mapx -= 15; // 이미지 움직이는 속도
	else
		Mapx = 1242; // 초기화
}

// 모든 키보드 처리 부분.
function KeyMove()
{
	// 키를 눌렸을 경우
	window.onkeydown = function(e) 
	{
		switch(e.keyCode) 
		{ // 플레이어 움직이는 부분 조절
		
					
				
			case 37: // 왼쪽
				if ( User.x > 0)
					User.x -= 10; 
				
			//	img[2] = img[5];
				break;
			case 39: // 오른족
				if ( User.x <= 700 )
					User.x += 10;
				
				//img[2] = img[6];
				break;
			case 38: // 위
				if ( User.y >= 0 )
					User.y -= 10;
				
				img[2] = img[5];
				
				break;
			case 40: // 아래
				if ( User.y <= 400 )
					User.y += 10;
				
				img[2] = img[6];
				
				break;
				
			case 65:
				/*for ( var i = 0 ; i < NUM ; i ++ )
					{
						if ( arMete[i].angle > 360)
							{
								arMete[i].angle = 0;
							}else{
								arMete[i].angle += 5;
							}
					}*/
				state = PROCESS_Start_2;
				break;
					
		
		}
	}
	
	// 키를 눌렸다가 풀었을 경우
	window.onkeyup = function(d)
	{
		switch ( d.keyCode)
		{
			case 37: // 왼쪽
			case 38: // 			
			case 39: // 오른쪽
			case 40: // 
	
				img[2] = img[4];
				break;
				
			
		}
	}
	
}

function Mete()
{ // 운석 초기 셋팅
	arMete.length = 0;
	

	for (var i = 0;i < NUM; i++)
			{
				arMete.push({
					x:900 + Math.random() * 500,
					y:15+(i*80),
					sw:60 ,
					sh:60 ,
					Num:Math.floor(Math.random() * 5), 
					angle: 10 ,
					Hp:5,
			
					
				});
			}

	for ( var i = 0 ; i < NUM ; i ++)
		{
			arMeteEffect.push(
			{
					SpriteImage:14,
					SpriteMin:0,
					SpriteMax:13,
					SpriteCount:0,
					x:-500,
					y:-500,
			});
		}
	
	


}

function MeteStruct()
{ // 운석 객체
	for (var i = 0;i < NUM; i++) 
	{ // 기본 객체 셋팅
		switch ( arMete[i].Num)
		{
			case 0 : // 기본
				arMete[i].x -= 7; // 속도
				arMete[i].sw = 50; // 충돌 범위
				arMete[i].sh = 50; // 충돌 범위
				arMete[i].Hp = 3; // 운석 체력
				break;
				
			case 1 : // 메테오
				arMete[i].x -= 12;
				arMete[i].sw = 75;
				arMete[i].sh = 75;
				arMete[i].Hp = 5;
				break;
				
			case 2: // 얼음
				arMete[i].x -= 12;
				arMete[i].sw = 50;
				arMete[i].sh = 50;
				arMete[i].Hp = 5;
				break;
				
			case 3: // 요상한
				arMete[i].x -= 15;
				arMete[i].sw = 50;
				arMete[i].sh = 50;
				arMete[i].Hp = 10;
				break;
				
			case 4: // 클립토나이트
				arMete[i].x -= 20;
				arMete[i].sw = 55;
				arMete[i].sh = 75;
				arMete[i].Hp = 75;
				break;
		}
		
		
		// 만약 운석의 x측 위치가 -100 이라면
		if (arMete[i].x < -100)  // 기본 700 + 랜덤 500정도 뒤에서 다시 나온다.
			{
				arMete[i].x = 900 + Math.random() * 500 ;
				arMete[i].Num = Math.floor(Math.random() * 4);
			}
		/*if (arMete[i].y > canvas.height+100) 
			arMete[i].y=0;
		if (arMete[i].y < -100) 
			arMete[i].y=canvas.height;*/
	}
	
	MeteCrash();// 운석 충돌
}

function MeteCrash()// *충돌처리
{	
	// 운석과 유저
	for ( var i = 0 ; i < NUM ; i ++ )
	{
				
		if (arMete[i].x > User.x-arMete[i].sw && 
			arMete[i].x < User.x+arMete[i].sw && 
			arMete[i].y > User.y-arMete[i].sh && 
			arMete[i].y < User.y+arMete[i].sh) 
		{
		//	state = PROCESS_End; // 엔딩 
		//	break;
		}
	}
	
	// 운석과 총알 -
	// 총알
	for ( var i = 0 ; i < UserBullet.length ; i ++ )
	{ // 운석-
		for ( var j = 0 ; j < NUM ; j ++ )
		{
		
			if (arMete[j].x > UserBullet[i].x-arMete[j].sw && 
				arMete[j].x < UserBullet[i].x+arMete[j].sw && 
				arMete[j].y > UserBullet[i].y-arMete[j].sh && 
				arMete[j].y < UserBullet[i].y+arMete[j].sh) 
			{
				
				arMeteEffect[j].x = arMete[j].x-arMete[j].sw/2 , arMeteEffect[j].y = arMete[j].y-arMete[j].sh/2;
				arMeteEffect[j].SpriteMin = 0;
				ctx.drawImage(img[arMeteEffect[j].SpriteImage], arMeteEffect[j].SpriteMin % 10 * 100, Math.floor(arMeteEffect[j].SpriteMin / 10 ) * 100,
				   	100, 100, arMeteEffect[j].x, arMeteEffect[j].y, 100, 100);
				
				// 운석 초기화
				arMete[j].x = 900 + Math.random() * 500 ;
				arMete[j].Num = Math.floor(Math.random() * 4);
			}
		}
	}

	// console.log(my);
}

function UserBulletCrate() // 총알 생성-
{
			
	UserBullet.length = 0;

	for (var i = 0;i < BulletCount; i++)
	{	 
				UserBullet.push(
					{
						x : User.x+130,
						y : User.y+40, 
						
					}
				);
			

	}
	
}

function UserBulletMove() // 총알 이동 및 초기화-
{	
	for ( var i = 0 ; i < UserBullet.length ; i ++ )
	{
				if ( UserBullet[i].x > 900 || UserBullet[i].x < 0 )
				{
					UserBullet[i].x = User.x + 130;
					UserBullet[i].y =User.y+40;
					
				}else{
				//	if ( img[2] == img[3] )
				//		UserBullet[i].x -= 40;
				//	else
						UserBullet[i].x += 40;
				}	
	}
	
	UserEffect.x = User.x-80;
	UserEffect.y = User.y+5;

}
function Start_2_Seting()
{
	if ( Start_2 )
		{
			for (var i = 0;i < NUM; i++)
			{
				arMete[i].Num = Math.floor(Math.random() * 4);
				console.log(arMete[i].Num);
			}
			Start_2 = false;
		}
		
}

function drawMain() 
{
	if (loadcount != Count)
	{
		ctx.font="30px arial";
		ctx.fillText("로딩중...", 100, 100);
		
	} else {
		ctx.drawImage(img[0], Mapx-1242, Mapy-240); // 배경화면 
		ctx.drawImage(img[1], Mapx+1242, Mapy-240); // 배경화면 
		ctx.drawImage(img[2], User.x, User.y); // 유 
	//	console.log(img[2]);
		
		// 운석
		for (var i = 0;i < NUM; i++) 
		{
			ctx.save();
			ctx.translate(arMete[i].x, arMete[i].y);
			ctx.rotate(arMete[i].angle * Math.PI / 180);
			ctx.translate(-arMete[i].x, -arMete[i].y);
			ctx.drawImage(img[7+arMete[i].Num], arMete[i].x, arMete[i].y); 
			ctx.restore();
 
		}
		
		// 총알
		for ( var j = 0 ; j < UserBullet.length ; j ++)
		{
			ctx.drawImage(img[12], UserBullet[j].x , UserBullet[j].y);
		}
		
		// 이펙트
		
		//유저 이펙트
		
		if ( UserEffect.SpriteMin < 101 ) // 잘했어요 이펙트
		{	
			UserEffect.SpriteCount ++ ;
			ctx.drawImage(img[UserEffect.SpriteImage], UserEffect.SpriteMin % 10 * 60, Math.floor(UserEffect.SpriteMin / 10 ) * 45,
				   	60, 45, UserEffect.x, UserEffect.y, 120, 90);
			if ( UserEffect.SpriteCount > 1 )
			{
					// console.log(EffectMotion.SpriteMin);
					UserEffect.SpriteMin = (UserEffect.SpriteMin +1) % UserEffect.SpriteMax;
					UserEffect.SpriteCount = 0;
			}
		}else{
			UserEffect.SpriteMin = 1;
			ctx.drawImage(img[UserEffect.SpriteImage], UserEffect.SpriteMin % 10 * 60, Math.floor(UserEffect.SpriteMin / 10 ) * 45,
				   	60, 45, UserEffect.x, UserEffect.y, 10, 90);
		}
		
		for ( var i = 0 ; i < NUM; i ++ )
		{
						// 운석 이펙트
			if ( arMeteEffect[i].SpriteMin < 12 ) // 잘했어요 이펙트
			{	
				arMeteEffect[i].SpriteCount ++ ;
				ctx.drawImage(img[arMeteEffect[i].SpriteImage], arMeteEffect[i].SpriteMin % 10 * 100, Math.floor(arMeteEffect[i].SpriteMin / 10 ) * 100,
				   	100, 100, arMeteEffect[i].x, arMeteEffect[i].y, 100, 100);
				if ( arMeteEffect[i].SpriteCount > 1 )
				{
					// console.log(EffectMotion.SpriteMin);
					arMeteEffect[i].SpriteMin = (arMeteEffect[i].SpriteMin +1) % arMeteEffect[i].SpriteMax;
					arMeteEffect[i].SpriteCount = 0;
				}
			}
		}

	/*	else{
			arMeteEffect.SpriteMin = 0;
			ctx.drawImage(img[arMeteEffect.SpriteImage], arMeteEffect.SpriteMin % 10 * 100, Math.floor(arMeteEffect.SpriteMin / 10 ) * 100,
				   	100, 100, arMeteEffect.x, arMeteEffect.y, 100, 100);
		}*/
		
		
	}
}










































































