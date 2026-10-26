import { GameListContainer } from "./components/GameListConteiner";

export const metadata = {
  title:"TOP | Steam Game Manager",
  description:"マイゲームライブラリの管理トップ画面です",
}

export default function Home() {
  return(<div><GameListContainer></GameListContainer></div>);
}