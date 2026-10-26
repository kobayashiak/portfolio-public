import React from "react";
import { SearchForm ,TotalCount} from "../components/GameListConteiner";


interface Props{
searchForm:SearchForm
totalCount:TotalCount
setSearchForm:(data:SearchForm)=>void;
handleSearch:(overridePage:number)=>void;
}



const pageNumber:React.FC<Props>=({searchForm,totalCount,handleSearch,setSearchForm})=>{


    const Pagenation = (event:React.MouseEvent<HTMLButtonElement>)=>{
        const nextPage = Number(event.currentTarget.value)
        handleSearch(nextPage)
        setSearchForm({...searchForm,page:nextPage})
    }
    const isFirstPage = searchForm.page ===1;

    const isLastpage = searchForm.page ===totalCount.max_page;

    return(<div className="flex pagenation items-center gap-4 mt-8 justify-center">
                <button className = "allow-box " 
                value={searchForm.page-1} onClick={Pagenation} disabled = {isFirstPage}>&laquo;</button>
                <div className="number-box min-w-12 text-center">
                <span className="text-xs text-slate-500 block leading-none mb-1 uppercase tracking-tighter font-bold">Page</span>
                <div className="number-box">{searchForm.page}</div>
                </div>
                <button className = "allow-box" value = {searchForm.page+1} onClick={Pagenation} disabled = {isLastpage}>&raquo;</button>

    </div>);
}

export default pageNumber;