POLICY = {
            'allowed': {
                    'modules':[
                        're', 'math', 'stat', 'random'
                    ],
            },
            'forbidden':{
                'builtins':[
                    'open', 'exit', 'compile', 'eval', 'file', 'execfile', 'input', 'memoryview', 'quit', 'globals', 'locals', 'vars'
                ],
            }
}