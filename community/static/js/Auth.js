$(".signup").on("shown.bs.modal", function() {
  $("#signupModal").trigger("focus");
});

//프로필 업로드
$(function() {
  $("#profile-image").click(function() {
    //이미지 클릭시
    $(".input-img").click(); //<input type="file" 파일 입력
    $(".input-img").on("change", handleIgmFileSelect); //변화 발생시 handleImgaFileSelect 함수 실행
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
