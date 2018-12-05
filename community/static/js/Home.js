var total_page = 1;
var now_page = 0;
var item_num = 4;
var sel_file;

/*글쓰기 버튼*/
function writePost() {
<<<<<<< HEAD
    document.write_post.submit();
=======
  var postContents = $("#input-post").val(); /*포스트 내용*/
  var username = "@CS.GG"; //글쓴이
  var writtenTime = "10 min ago"; //글쓴 시간
  var imgSrc = "https://picsum.photos/50/50"; //프로필 사진

  if (postContents != "") {
    $(".gedf-card-row").append(
      `<div class="card gedf-card post-card" id="posts-partition">
        <div class="card-header">
          <div class="d-flex justify-content-between align-items-center">
            <div class="d-flex justify-content-between align-items-center">
              <div class="mr-2">
                <img
                  class="rounded-circle"
                  width="45"
                  src=` +
        imgSrc +
        `
                  alt=""
                />
              </div>
              <div class="ml-2">
                <div class="h5 m-0">` +
        username +
        `</div>
                <div class="h7 text-muted">Computer Science.Good Game</div>
              </div>
            </div>
          </div>
        </div>

        <div class="card-body">
          <div class="text-muted h7 mb-2">
            <i class="fa fa-clock-o"></i>` +
        writtenTime +
        `(게시시간)
          </div>
        <p class="card-text">` +
        postContents +
        `</p>
        </div>
        <div class="card-footer">
          <a href="#" class="card-link">
          <i class="fa fa-gittip"></i> Like
          </a>
        </div>
      </div>`
    );
  }
  if (
    $(".post-card:visible").length / 4 > clickCount &&
    $(".post-card:visible").length / 4 < clickCount + 1
  ) {
    $(".gedf-card:hidden").show();
  }
  if ($(".gedf-card:hidden").length > 0) {
    $("#Viewmore").css("display", "block");
  }
>>>>>>> upstream/master
}

// //더보기
// function viewmorePosts(event) {
//     clickCount += 1;
//     event.preventDefault();
//     $(".gedf-card:hidden")
//         .slice(0, 4)
//         .show();
//     if ($(".gedf-card:hidden").length == 0) {
//         $("#Viewmore").css("display", "none");
//     }
// }

//페이지 렌더링
$(function () {
    $(".gedf-card")
        .slice(0, 4)
        .show();
    // $("#Viewmore").click(viewmorePosts);
});

//프로필 업로드
<<<<<<< HEAD
$(function () {
    //이미지 클릭시
    $("#profile-image").click(function () {
        //<input type="file" 파일 입력
        $(".input-img").click();
        $(".input-img").on("change", handleImgFileSelect); //변화 발생시 handleImgaFileSelect 함수 실행
    });

    lastPostFunc();

    $(window).scroll(function () {
        event.preventDefault();
        console.log($(window).scrollTop(), " ", $(document).height() - $(window).height())
        if ($(window).scrollTop() > $(document).height() - $(window).height()) {
            lastPostFunc();
        }
    });
});

function handleImgFileSelect(event) {
    var files = event.target.files;
    var filesArr = Array.prototype.slice.call(files);

    filesArr.forEach(function (f) {
        if (!f.type.match("image.*")) {
            alert("이미지만 사용가능합니다.");
            return;
        }
        sel_file = f;

        var reader = new FileReader();
        reader.onload = function (event) {
            $("#profile-image").attr("src", event.target.result);
        };
        reader.readAsDataURL(f);
    });
}

function lastPostFunc() {
   now_page++;
   if (now_page > total_page){
       $(window).scroll(null);
       $('.loading-text').remove();
   }else{
       $.ajax({
        url: "rest/getPost?user_id=" + _page_id + "&item_num="+item_num+"&page="+now_page,
        type: 'get',
        success: function (data) {
            total_page = data.total_page;
            now_page = data.now_page;
            for (let i = 0; i < data.data.length; i++) {
                writePost(data.data[i].post);
            }
        }
    })
   }
}

function writePost(arr) {
  var postContents = arr.content; /*포스트 내용*/
  var username = "@"+_page_id; //글쓴이
  var nickname = _nickname; //닉네임
  var writtenTime = new Date(arr.date); //글쓴 시간
  console.log(writtenTime);
  var imgSrc = _user_img; //프로필 사진

  if (postContents != "") {
    $(".gedf-card-row").append(
      `<div class="card gedf-card post-card" id="posts-partition">
        <div class="card-header">
          <div class="d-flex justify-content-between align-items-center">
            <div class="d-flex justify-content-between align-items-center">
              <div class="mr-2">
                <img
                  class="rounded-circle"
                  width="45"
                  src=` +
        imgSrc +
        `
                  alt=""
                />
              </div>
              <div class="ml-2">
                <div class="h5 m-0">` +
        username +
        `</div>
                <div class="h7 text-muted">`+nickname+`</div>
              </div>
            </div>
          </div>
        </div>

        <div class="card-body">
          <div class="text-muted h7 mb-2">
            <i class="fa fa-clock-o"></i>` +
        writtenTime.toDateString() +
        `
          </div>
        <p class="card-text">` +
        postContents +
        `</p>
        </div>
        <div class="card-footer">
          <a href="#" class="card-link">
          <i class="fa fa-gittip"></i> Like
          </a>
        </div>
      </div>`
    );
  }
  $(".gedf-card:hidden").show();
}

function handleFollowButton(event) {
    let id = $('#follow').attr('user');

    $.ajax({
        url: "auth/toggleFollow?id=" + id,
        type: 'get',
        success: function (data) {
            let obj = data;
            if (obj.code === 0) {
                $("#follow").removeClass('Followed');
                $("#follow").html("Follow");
            } else {
                $("#follow").addClass('Followed');
                $("#follow").html("Following");
            }
            $("#follower").html(obj.follower);
            $("#following").html(obj.following);
        }
    })
=======
$(function() {
  //이미지 클릭시
  $("#profile-image").click(function() {
    //<input type="file" 파일 입력
    $(".input-img").click();
    $(".input-img").on("change", handleImgFileSelect); //변화 발생시 handleImgaFileSelect 함수 실행
  });
});

function handleImgFileSelect(event) {
  var files = event.target.files;
  var filesArr = Array.prototype.slice.call(files);

  filesArr.forEach(function(f) {
    if (!f.type.match("image.*")) {
      alert("이미지만 사용가능합니다.");
      return;
    }
    sel_file = f;

    var reader = new FileReader();
    reader.onload = function(event) {
      $("#profile-image").attr("src", event.target.result);
    };
    reader.readAsDataURL(f);
  });
>>>>>>> upstream/master
}

function handleFollowButton(event) {
  if ($(".follow").html() === "Follow") {
    $(".follow").html("Following");
    $(".follow").css("background-color", "#2bac85");
    $(".follow").css("color", "#ffffff");
  } else {
    $(".follow").html("Follow");
    $(".follow").css("background-color", "#ffffff00");
    $(".follow").css("color", "#2bac85");
  }
}
