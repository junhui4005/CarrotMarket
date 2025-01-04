<script>
    import Main from "./pages/Main.svelte";
    import Login from "./pages/Login.svelte";
    import Singup from "./pages/Signup.svelte";
    import Write from "./pages/Write.svelte";
    import Router from "svelte-spa-router";
    // @ts-ignore
    import NotFound from "./pages/NotFound.svelte";
    // @ts-ignore
    import Loading from "./pages/Loading.svelte";
    import "./css/style.css";
    import {
      GoogleAuthProvider,
      getAuth,
      signInWithCredential,
    } from "firebase/auth";
    import { user$ } from "./store";
    import { onMount } from "svelte";
    // @ts-ignore
    import MyPage from "./pages/MyPage.svelte";
  
    let isLoading = true;
  
    // 토큰을 이용한 소셜 로그인
    const checkLogin = async () => {
      const auth = getAuth();
      const token = localStorage.getItem("token"); // access token
      if (!token) return (isLoading = false);
  
      try {
        const credential = GoogleAuthProvider.credential(null, token);
        const result = await signInWithCredential(auth, credential);
        const user = result.user;
        user$.set(user);
        isLoading = false;
      } catch (error) {
        user$.set(null);
        localStorage.removeItem("token");
        window.location.hash = "/login";
      }
    };
  
    // router 설정
    const routes = {
      "/": Main,
      "/signup": Singup,
      "/write": Write,
      "/my": MyPage,
      "*": NotFound,
    };
  
    // 렌더링될 때마다 동작
    onMount(() => checkLogin());
  </script>
  
  {#if isLoading}
    <Loading />
  {:else if !$user$}
    <Login />
  {:else}
    <Router {routes} />
  {/if}
  <!-- 
  <main>
    <div>안녕하세요!</div>
  </main>
  
  <style>
    div {
      color : red;
    }
  </style> -->