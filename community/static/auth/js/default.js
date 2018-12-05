function sign_up() {
    is_check = $('#btn_id_check').hasClass('btn-success');
    if(is_check){
        document.signup.submit();
    }else{
        alert("아이디 중복검사를 해주세요");
    }
}

$(".signup").on("shown.bs.modal", function() {
  $("#signupModal").trigger("focus");
});

function check_id() {
    $('#btn_id_check').removeClass('btn-danger');
    $('#btn_id_check').removeClass('btn-success');
    id = $('#signupID').val();
    $.ajax({
        url: "auth/checkId?id="+id,
        type: 'get',
        success: function (data) {
            let obj = data
            if(obj.code === 1){
                $('#btn_id_check').removeClass('btn-danger');
                $('#btn_id_check').addClass('btn-success');
            }else{
                $('#btn_id_check').removeClass('btn-success');
                $('#btn_id_check').addClass('btn-danger');
            }
        }

    })
}

function change_id(){
    $('#btn_id_check').removeClass('btn-danger');
    $('#btn_id_check').removeClass('btn-success');
}

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
      $(".input-img").val('');
      return ;
    }
    sel_file = f;

    var reader = new FileReader();
    reader.onload = function(event) {
      $("#profile-image").attr("src", event.target.result);
    };
    reader.readAsDataURL(f);
  });
}

