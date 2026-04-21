from route import test
from base_response import succes_response, error_response
@test.get('/')
async def test_route():
    ans = "test"
    return succes_response(message=ans)