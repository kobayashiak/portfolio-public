import { Tag } from "@/app/types/game"
interface Props{
    tag:Tag
}

export const TagListItem = ({tag}:Props)=>{
    return(
        <div className = 'bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded'>
        <span>{tag.name}</span>
        </div>
    )
}