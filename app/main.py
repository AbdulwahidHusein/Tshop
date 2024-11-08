from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cart.routes import  cart_router
from user.routes import user_router
from store.routes import store_router
from product.routes import product_router

app = FastAPI()

# Middleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(cart_router, prefix="/api/v1", tags=["Cart"])
app.include_router(user_router, prefix="/api/v1", tags=["User"])
app.include_router(store_router, prefix="/api/v1", tags=["Store"])
app.include_router(product_router, prefix="/api/v1", tags=["Product"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


