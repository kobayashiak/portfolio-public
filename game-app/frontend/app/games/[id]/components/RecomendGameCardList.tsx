import { Game } from "@/app/types/game"
import { RecommendedGameCard } from "./RecommendGameCard"

interface Props{
    recommendGames:Game[]
}


export const RecommendedGameCardList = ({recommendGames}:Props)=> {
    if(!recommendGames || recommendGames.length ===0) return null;
return(<section className="mt-12">
    <div className="flex items-center gap-2 mb-6">
        <div className="w-1 h-6 bg-blue-500 rounded-full"/>
        <h3 className="text-xl font-bold text-white tracking-wide">
            あなたへのおすすめ
        </h3>
    </div>
<div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6'>
    {recommendGames.map((recommendGame)=>(<RecommendedGameCard key={recommendGame.id} game={recommendGame}/>))}
    </div></section>)
}