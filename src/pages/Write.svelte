<script>
    import Footer from "../components/Footer.svelte";
    import { getDatabase, ref, push, set, refFromURL } from "firebase/database";
    import {
      getStorage,
      ref as refImage,
      uploadBytes,
      getDownloadURL,
    } from "firebase/storage";
  
    // database
    let title;
    let price;
    let description;
    let place;
  
    function writeUserDate(imgUrl) {
      const db = getDatabase();
      push(ref(db, "items/"), {
        // push를 이용해서 자동으로 key값 추가
        imgUrl,
        title,
        price,
        insertAt: new Date().getTime(),
        description,
        place,
      });
      alert("글쓰기가 완료되었습니다."); // 안쓰는 문법
      window.location.hash = "/";
    }
  
    // 테스트 버튼
    // function writeUserData(userId, name, email) {
    //   const db = getDatabase();
    //   set(ref(db, "users/" + userId), {
    //     username: name,
    //     email: email,
    //   });
    // }
  
    // image 업로드
    const storage = getStorage();
  
    let files;
    const uploadFile = async () => {
      const file = files[0];
      const name = file.name;
      const storageRef = refImage(storage, name);
      await uploadBytes(storageRef, file);
      const url = await getDownloadURL(storageRef);
      return url;
    };
  
    const handleSubmit = async () => {
      const imgUrl = await uploadFile();
      writeUserDate(imgUrl);
    };
  </script>
  
  <!-- firebase는 no-sql 구조 -->
  <!-- <button on:click={() => writeUserData("abc", "me", "abc@gmail.com")}>
    테스트
  </button> -->
  
  <form id="write-form" on:submit|preventDefault={handleSubmit}>
    <div>
      <label for="image">이미지</label>
      <input type="file" bind:files id="image" name="image" />
    </div>
    <div>
      <label for="title">제목</label>
      <input type="text" id="title" name="title" bind:value={title} />
    </div>
    <div>
      <label for="price">가격</label>
      <input type="number" id="price" name="price" bind:value={price} />
    </div>
  
    <div>
      <label for="description">설명</label>
      <input
        type="text"
        id="description"
        name="description"
        bind:value={description}
      />
    </div>
    <div>
      <label for="place">장소</label>
      <input type="text" id="place" name="place" bind:value={place} />
    </div>
    <div>
      <div>
        <button class="write-button" type="submit">글쓰기 완료</button>
      </div>
    </div>
  </form>
  
  <Footer location="Write" />
  
  <style>
    .write-button {
      background-color: aqua;
      margin: 10px;
      border-radius: 10px;
      padding: 5px 12px 5px 12px;
      cursor: pointer;
    }
  </style>