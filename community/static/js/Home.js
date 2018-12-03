var clickCount = 0;
var sel_file;
/*글쓰기 버튼*/
function writePost() {
  document.write_post.submit();
}

//더보기
function viewmorePosts(event) {
  clickCount += 1;
  event.preventDefault();
  $(".gedf-card:hidden")
    .slice(0, 4)
    .show();
  if ($(".gedf-card:hidden").length == 0) {
    $("#Viewmore").css("display", "none");
  }
}

//페이지 렌더링
$(function() {
  $(".gedf-card")
    .slice(0, 4)
    .show();
  $("#Viewmore").click(viewmorePosts);
});

//프로필 업로드
$(function() {
  $("#profile-image").click(function() {
    $(".input-img").click();
    $(".input-img").on("change", handleIgmFileSelect);
  });
});

function handleIgmFileSelect(event) {
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
}
