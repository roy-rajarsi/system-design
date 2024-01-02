from auth_flows.simple_auth_flow import SimpleAuthFlow
from auth_flows.rate_limited_auth_flow import RateLimitedAuthFlow


def main() -> None:
    simple_auth_flow: SimpleAuthFlow = SimpleAuthFlow()
    response = simple_auth_flow.process_auth_request({'username': 'demo_user1',
                                                      'password': 'demo_user1_password'
                                                      })
    print(response)

    rate_limited_auth_flow: RateLimitedAuthFlow = RateLimitedAuthFlow()
    response = rate_limited_auth_flow.process_auth_request({'username': 'demo_user1',
                                                            'password': 'demo_user1_password'
                                                            })
    print(response)

    response = rate_limited_auth_flow.process_auth_request({'username': 'admin_user1',
                                                            'password': 'admin_user1_password',})

    print(response)


if __name__ == '__main__':
    main()
