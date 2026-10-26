import React from "react";
import Link from "next/link";

import {Game} from  "../types/game"


interface GameListProps{
    games:Game[];
}

interface GameProps{
    game:Game;
}

const GameInfo:React.FC<GameProps> = ({game})=>{
    return(<div className="flex items-center justify-between p-3 bg-[#1b2838]/40 border-b border-slate-800 hover:bg-[#2a475e]/40 transition-all group">
        <div className="flex items-center gap-4"><Link href ={`/games/${game.id}`} className="text-slate-200 font-medium hover:text-[#66c0f4] transition-colors line-clamp-1">{game.name}</Link></div>
        
        <div className="flex items-center gap-4 text-sm" ><span className="text-slate-400">実績解除率:</span><span className="text-[#66c0f4] font-mono">{game.complete_rate}%</span></div>

    </div>)
}

const GameList:React.FC<GameListProps> = ({games})=>{
    return(<div className = "flex flex-col gap-4 p-4 bg-[#1b2838]/20 border border-slate-800/50 rounded-sm shadow-2xl">
            {games.map((game) =>(<GameInfo key ={game.id} game={game}/>))}
        </div>);
} 

export default GameList