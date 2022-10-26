function logout() {
  document.cookie = 'account=; expires=Thu, 01 Jan 1970 00:00:01 GMT;domain=localhost; path=/'
  alert("로그아웃 되었습니다.")
  location.href = "/";
}

function validate_user() {
  if (document.cookie != '') {
    $("#login-button").text('로그아웃');
    $("#login-button").attr('onclick', "logout()");

    let temp_html = `<button class="login-button border ms-2" onclick="location.href='/mypage'">마이페이지</button>`;
    $("#log-info").append(temp_html);

  } else {
    $("#login-button").text('로그인');
  }
}