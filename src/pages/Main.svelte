<script>
    import { onMount } from "svelte";
    import Footer from "../components/Footer.svelte";
    import { getDatabase, ref, onValue } from "firebase/database";
  
    const time = new Date();
    let currentTime = time.getHours() + ":" + time.getMinutes();
  
    // 1초마다 1씩 더해지는 코드
    // setInterval(() => (currentTime = currentTime + 1), 1000);
  
    $: items = []; // 반응형 변수
  
    const db = getDatabase();
    const itemsRef = ref(db, "items/");
  
    onMount(() => {
      onValue(itemsRef, (snapshot) => {
        const data = snapshot.val();
        items = Object.values(data).reverse();
      });
    });
  
    // 시간 계산하기
    const calcTime = (timestamp) => {
      // 한국시간 UTC+9 : getTime()
      const curTime = new Date().getTime() - 9 * 60 * 60 * 1000; // 세계시간으로 변경
      const time = new Date(curTime - timestamp);
      const hour = time.getHours();
      const minutes = time.getMinutes();
      const seconds = time.getSeconds();
  
      if (hour > 0) return `${hour}시간 전`;
      else if (minutes > 0) return `${minutes}분 전`;
      else if (seconds > 0) return `${seconds}초 전`;
      else return "방금전";
    };
  </script>
  
  <header>
    <div class="info-bar">
      <div class="info-bar__time">{currentTime}</div>
      <div class="info-bar__icons">
        <img src="assets/chart-bar.svg" alt="chart-bar" />
        <img src="assets/wifi.svg" alt="wifi" />
        <img src="assets/battery.svg" alt="battery" />
      </div>
    </div>
    <div class="menu-bar">
      <div class="menu-bar__location">
        <div>역삼1동</div>
        <div class="menu-bar__location_icon">
          <img src="assets/arrow.svg" alt="donw-arrow" />
        </div>
      </div>
      <div class="menu-bar__icons">
        <img src="assets/search.svg" alt="search" />
        <img src="assets/menu.svg" alt="menu" />
        <img src="assets/alert.svg" alt="alert" />
      </div>
    </div>
  </header>
  
  <main>
    {#each items as item}
      <div class="item-list">
        <div class="item-list__img">
          <img src={item.imgUrl} alt={item.title} />
        </div>
        <div class="item-list__info">
          <div class="item-list__info-title">{item.title}</div>
          <div class="item-list__info-meta">
            {item.place}
            {calcTime(item.insertAt)}
          </div>
          <div class="item-list__info-price">{item.price}</div>
          <div class="item-list__info-description">{item.description}</div>
        </div>
      </div>
    {/each}
  
    <a class="write-btn" href="#/write">+글쓰기</a>
  </main>
  
  <Footer location="home" />
  
  <div class="media-info-msg">화면 사이즈를 줄여주세요</div>
  
  <style>
    .info-bar__time {
      color: red;
    }
  </style>