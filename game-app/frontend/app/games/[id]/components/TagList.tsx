import {Tag} from '../../../types/game'
import { TagListItem } from './TagListItem'

interface Props{
tags:Tag[]
}


export const TagList = ({tags}:Props)=>{
return(<div className='flex flex-wrap gap-2'>
    {tags.map((tag)=>(
        <span key={tag.id}><TagListItem tag={tag}></TagListItem></span>
    ))}
</div>)
}