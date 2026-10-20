import { createContext,useContext,useState } from "react";

const AIProviderContext = createContext(null);

export function AIProviderProvider({children}){
    const [provider,setProvider] = useState("gogle");

    return (<AIProviderContext.Provider value = {{provider,setProvider}}>
        {children}
    </AIProviderContext.Provider>
    )
}

export function useAIProvider(){
    return useContext(AIProviderContext);
}