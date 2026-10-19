import { useContext,useState,useEffect,createContext } from "react";

const AuthContext = createContext(null);

export default function AuthProvider({children}){

    const [user,setUser] = useState(null);
    const [loading,setLoading] = useState(true);

    async function fetchCurrentUser() {
        try{
            const response = await fetch("http://localhost:8000/login/me",
                {credentials :"include"}
            );

                if (!response.ok) {
            console.error(
                "Authentication failed:",
                response.status,
                await response.text()
            );
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
    



    
 async   function logout(){
        try{
            await fetch("http://localhost:8000/login/logout",{
                method:"POST",
                credentials:"include",
            });
        }catch(error){
            console.error("Backend logout failed:",error)
        }finally{
   
        setUser(null);
        window.location.replace("/login");
    }
}
    useEffect(() => {
        fetchCurrentUser();

        function handleSessionExpired() {
        setUser(null);
        window.location.replace("/login");
        }

        window.addEventListener(
        "auth:session-expired",
        handleSessionExpired
        );

        return () => {
        window.removeEventListener(
            "auth:session-expired",
            handleSessionExpired
        );
        };
    }, []);


    const isAuthenticated = Boolean(user);

    return (<AuthContext.Provider value = {{user,setUser,isAuthenticated,loading,logout,fetchCurrentUser}}>
        {children}
        </AuthContext.Provider>);
}

export function useAuth(){
    return useContext(AuthContext);
}
