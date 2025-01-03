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

// 판매되는 이미지 출력하기
const renderDate = (data) => {
  const main = document.querySelector("main");

  // reverse() 배열 뒤집기
  data.reverse().forEach(async (obj) => {
    const div = document.createElement("div");
    div.className = "item-list";

    const infoDiv = document.createElement("div");
    infoDiv.className = "item-list__info";

    const imgDiv = document.createElement("div");
    imgDiv.className = "item-list__img";

    const img = document.createElement("img");
    const res = await fetch(`/image/${obj.id}`);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob); // url 생성
    img.src = url;

    const itemListInfoTitleDiv = document.createElement("div");
    itemListInfoTitleDiv.className = "item-list__info-title";
    itemListInfoTitleDiv.innerText = obj.title;

    const itemListInfoMetaDiv = document.createElement("div");
    itemListInfoMetaDiv.className = "item-list__info-meta";
    itemListInfoMetaDiv.innerText = obj.place + " " + calcTime(obj.insertAt);

    const itemListInfoPriceDiv = document.createElement("div");
    itemListInfoPriceDiv.className = "item-list__info-price";
    itemListInfoPriceDiv.innerText = obj.price;

    imgDiv.appendChild(img);
    infoDiv.appendChild(itemListInfoTitleDiv);
    infoDiv.appendChild(itemListInfoMetaDiv);
    infoDiv.appendChild(itemListInfoPriceDiv);
    div.appendChild(imgDiv);
    div.appendChild(infoDiv);
    main.appendChild(div);
  });
};

// 서버로부터 데이터받아오기
const accessToken = window.localStorage.getItem("token");
const fetchList = async () => {
  const res = await fetch("/items", {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  console.log(res.status);
  if (res.status == 401) {
    alert("로그인이 필요합니다!");
    window.location.pathname = "/login.html";
    return;
  }

  const data = await res.json();
  renderDate(data);
};

fetchList();