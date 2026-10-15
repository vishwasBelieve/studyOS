import { useContext,useState,useEffect,createContext } from "react";

const AuthContext = createContext(null);

export default function AuthProvider({children}){

    const [user,setUser] = useState(null);
    const [loading,setLoading] = useState(true);

    async function fetchCurrentUser() {
        try{
            const response = await fetch("http://127.0.0.1:8000/login/me",
                {credentials :"include"}
            );

            if(!response.ok){
                setUser(null);
                return;
            }
            const data = await response.json()
            setUser(data);

        }
        catch(error){
            console.error("Failed to check authentication:",error);
            setUser(null);
        }finally{
            setLoading(false);
        }
    }
    
    useEffect(()=>{fetchCurrentUser();},[]);



    
    function logout(){
   
        setUser(null);
    }

    const isAuthenticated = Boolean(user);

    return (<AuthContext.Provider value = {{user,setUser,isAuthenticated,loading,logout,fetchCurrentUser}}>
        {children}
        </AuthContext.Provider>);
}

export function useAuth(){
    return useContext(AuthContext);
}
