# coap_server.py — Localhost CoAP file server
import asyncio
from aiocoap import resource, Context, Message

class FileResource(resource.Resource):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    async def render_get(self, request):
        print(f"➡️ Request received for {self.filename}")
        try:
            with open(self.filename, "rb") as f:
                data = f.read()
            print(f"📤 Sending {len(data)} bytes from {self.filename}")
            return Message(payload=data)
        except Exception as e:
            print(f"❌ Error reading {self.filename}: {e}")
            return Message(payload=str(e).encode())

async def main():
    root = resource.Site()

    # register resources exactly matching your file names
    root.add_resource(("100B",), FileResource("100B"))
    root.add_resource(("10KB",), FileResource("10KB"))
    root.add_resource(("1MB",), FileResource("1MB"))
    root.add_resource(("10MB",), FileResource("10MB"))

    # bind to localhost
    await Context.create_server_context(root, bind=("127.0.0.1", 5683))
    print("✅ CoAP server running on 127.0.0.1:5683 ...")

    # keep server running forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
