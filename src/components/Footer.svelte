<script>
    export let location;
  
    const moveToHome = () => {
      window.location.hash = "/";
      location = "home";
    };
  
    const moveToMyPage = () => {
      window.location.hash = "/my";
      location = "myPage";
    };
  </script>
  
  <footer>
    <div class="footer-block">
      <button class="footer-icons" on:click={moveToHome}>
        <div class="footer-icons__img">
          {#if location === "home"}
            <img src="assets/home-full.svg" alt="home" />
          {:else}
            <img src="assets/home.svg" alt="home" />
          {/if}
        </div>
        <div class="footer-icons__desc">홈</div>
      </button>
      <div class="footer-icons">
        <div class="footer-icons__img">
          <img src="assets/document.svg" alt="document" />
        </div>
        <div class="footer-icons__desc">동네생활</div>
      </div>
      <div class="footer-icons">
        <div class="footer-icons__img">
          <img src="assets/map.svg" alt="map" />
        </div>
        <div class="footer-icons__desc">내 근처</div>
      </div>
      <div class="footer-icons">
        <div class="footer-icons__img">
          <img src="assets/chat.svg" alt="char" />
        </div>
        <div class="footer-icons__desc">채팅</div>
      </div>
      <button class="footer-icons" on:click={moveToMyPage}>
        <div class="footer-icons__img">
          {#if location === "myPage"}
            <img src="assets/user-full.svg" alt="user" />
          {:else}
            <img src="assets/user.svg" alt="user" />
          {/if}
        </div>
        <div class="footer-icons__desc">나의 당근</div>
      </button>
    </div>
  </footer>