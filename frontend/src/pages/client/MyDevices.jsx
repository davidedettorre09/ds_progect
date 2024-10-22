import { useEffect, useState } from "react";
import deviceServices from "../../services/deviceServices";

const MyDevices = () => {
    const [allDevices, setAllDevices] = useState([])
    const [isLoadingDevices, setIsLoadingDevices] = useState(false);
    const [errorDevices, setErrorDevices] = useState(null);
    const { getAllClientDevices } = deviceServices;

    useEffect(()=>{
        const fetchData = async () => {
            setIsLoadingDevices(true);
            setErrorDevices(null);
            try {
              const response = await getAllClientDevices();
              setAllDevices(response);
            } catch (error) {
              setErrorDevices(error);
            } finally {
              setIsLoadingDevices(false);
            }
          };
          fetchData();
      
    }, [])

  return (
    <>
    <div className="grid mt-4">
      <div className="col-100">
        <h1>My Devices</h1> <br />
      </div>
    </div>
    <div className="grid mt-2">    
        {isLoadingDevices && <p>Loading...</p>}
        {errorDevices && <p>Error: {errorDevices.message}</p>}
        {allDevices && allDevices.length > 0 && allDevices.map((device)=>(
            <div className="col-33" key={device?.id}>
              <h4>{device?.description}</h4>
               <p>Address: {device?.address}</p>
              <p>Mac Hourly Consuption: {device?.max_hourly_consumption}</p>
              <p>Owner: {device?.owner_id}</p>
            </div>
        ))}
        {!allDevices || allDevices.length <= 0 && <p>No device</p> }
    </div>
    </>
  )


}

export default MyDevices