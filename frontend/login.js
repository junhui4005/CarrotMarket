const form = document.querySelector("#login-form");

// 로그인하기
const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);

  // 서버 요청
  const res = await fetch("/login", {
    method: "post",
    body: formData,
  });

  // 로그인 요청 성공 시
  const data = await res.json();
  const accessToken = data.access_token;
  console.log(data);
  if (res.status === 200) {
    // 로그인 성공해서 items 가져오기
    // const infoDiv = document.querySelector("#info");
    // infoDiv.innerText = "로그인에 성공했습니다.";

    // const btn = document.createElement("button");
    // btn.innerText = "상품 가져오기!";
    // btn.addEventListener("click", async () => {
    //   const res = await fetch("/items", {
    //     headers: {
    //       Authorization: `Bearer ${accessToken}`,
    //     },
    //   });
    //   const data = await res.json();
    //   console.log(data);
    // });
    // infoDiv.appendChild(btn);

    alert("로그인에 성공했습니다.");
    window.localStorage.setItem("token", accessToken);
    // window.sessionStorage.setItem("token", accessToken); // 브라우저 창 제거 시 삭제됨
    console.log(res.status);
    window.location.pathname = "/";
  } else if (res.status === 401) {
    // 로그인 실패 시
    alert("id 또는 password가 틀렸습니다.");
  }
};

form.addEventListener("submit", handleSubmit);