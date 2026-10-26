import { Achievement } from "@/app/types/game"
import { AchievementListItem } from "./AchievementListItem"

interface Props{
    achievements:Achievement[]
}

export const AchievementList = ({achievements}:Props)=>{

    const total = achievements.length;
    const unlockCount = achievements.filter((a)=>a.unlocktime>0).length

    return(<div className="leading-none">
    <h3 className="text-xs text-slate-500 font-bold tracking-widest mb-3">実績リスト</h3>
    <div className="text-xl text-sky-400 font-bold">開放状況:{unlockCount}/{total}</div>  
    <div className="max-h-100 overflow-y-auto pr-2 space-y-2 bg-slate-900 border-sky-800 border-4 rounded-sm custom-scrollbar">
        {achievements.map((achievement)=>(<AchievementListItem key={achievement.id} achievement={achievement}></AchievementListItem>))}

    
    
    </div></div>)
}