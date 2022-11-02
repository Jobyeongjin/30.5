// 네비게이션 바 

function navigo() {
  const header = document.querySelector('nav'); //헤더부분획득
  const headerheight = header.clientHeight;//헤더높이

  document.addEventListener('scroll', onScroll, { passive: true });//스크롤 이벤트

  function onScroll() {
      const scrollposition = pageYOffset;//스크롤 위치
      const nav = document.querySelector('nav');//네비게이션

      if (headerheight <= scrollposition) {//만약 헤더높이<=스크롤위치라면
          nav.classList.add('fix')//fix클래스를 네비에 추가
      }
      else {//그 외의 경우
          nav.classList.remove('fix');//fix클래스를 네비에서 제거
      }
  }
}
navigo()