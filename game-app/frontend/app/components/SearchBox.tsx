import {Game} from '../types/game'
import {SearchForm,sortOptions,options} from '../components/GameListConteiner'



interface Props{
    searchForm:SearchForm,
    setSearchForm:(data:SearchForm) => void;
    handleSearch:(overridePage?:number) =>void
    
}

const SearchBox:React.FC<Props> = ({searchForm,setSearchForm,handleSearch})=>{
    
    const handleChange = (event:React.ChangeEvent<HTMLSelectElement>) =>{
        setSearchForm({...searchForm,selectedOption:event.target.value})
    };

    const handleChangeSorted = (event:React.ChangeEvent<HTMLSelectElement>)  =>{
        setSearchForm({...searchForm,selectedSortOption:event.target.value})
    }

    const handleInput = (event:React.ChangeEvent<HTMLInputElement>) =>{
        setSearchForm({...searchForm,word:event.target.value})
    }



    return (<div className = "flex flex-col gap-3 w-full max-w-4xl">
            <div className="flex items-center p-1 bg-[#101822]/90 border-t-[#4a5568] border-l-[#4a5568]  border-b-[#1a202c] border-r-[#1a202c]  rounded-sm shadow-[inset_0_2px_4px_rgba(0,0,0,0.9),0_1px_0_rgba(255,255,255,0.05)] focus-within:border-[#66c0f4] transition-all">
                <input value={searchForm.word} type="text" placeholder="検索..." className="flex-1 bg-transparent outline-none px-4 py-2 text-slate-200 placeholder:text-slate-500" onChange={handleInput}></input>
                <button className = "btn-base" onClick={ ()=>{handleSearch()}}>検索</button>
            </div>
            <div className = 'flex gap-2 w-full'>
                <select value={searchForm.selectedOption} onChange={handleChange} className='pulldown'>
                    {options.map((option) => (<option key = {option.value} value={option.value}>{option.column}</option>))}

                </select>
                <select value ={searchForm.selectedSortOption} onChange={handleChangeSorted} className='pulldown'>
                    {sortOptions.map((sortOption) => (<option key = {sortOption.value} value = {sortOption.value}>{sortOption.sort}</option>))}
                </select>
            </div>
        </div>)
}



export default SearchBox;