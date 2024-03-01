import settings
import uvicorn
from fastapi import FastAPI, HTTPException
from ram_utils import DataStore, DBInteractionException, RAMStatsCollector

app = FastAPI()
store = DataStore(settings.SETTINGS['db']['path'])
store.create_table()

ram_monitoring_interval = int(settings.SETTINGS['server']['ram_monitoring_interval'])
host = settings.SETTINGS['server']['host']
port = settings.SETTINGS['server']['port']


@app.get("/get_last_usage")
async def get_last_n_ram_usage(n: int):
    try:
        return store.get_last_n_records(n)
    except DBInteractionException:
        raise HTTPException(status_code=500, detail="Something bad occurred.")


@app.on_event("shutdown")
def shutdown_event():
    store.teardown()


if __name__ == "__main__":
    ram_collector = RAMStatsCollector(interval_seconds=ram_monitoring_interval)
    ram_collector.store_ram_job()
    uvicorn.run(app, host=host, port=port)
