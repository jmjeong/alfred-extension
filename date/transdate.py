"""transdate -- Python implementation of Asian lunisolar calendar
Copyright (c) 2004-2006, Kang Seonghoon aka Tokigun.

This module declares lunardate class which represents a day of Asian
lunisolar calendar. lunardate class is compatible with datetime.date
class, so you can use both lunardate and date interchangeably.

lunardate class can handle date between 1881-01-30 (lunar 1881-01-01)
and 2051-02-10 (lunar 2050-12-29). Since lunisolar calendar table is
based on Korea Astronomy & Space Science Institute, it can be
different with calendars used by other countries.

In order to reduce size of bytecode, all of numeric table is stored as
Unicode string (capable for range between 0 and 65535). If your Python
is not compiled with Unicode, use transdate_nounicode.py instead.
"""

__author__ = 'Kang Seonghoon aka Tokigun'
__version__ = '1.1.1 (2006-06-25)'
__copyright__ = 'Copyright (c) 2004-2006 Kang Seonghoon aka Tokigun'
__license__ = 'LGPL'

__all__ = ['sol2lun', 'lun2sol', 'date', 'timedelta', 'solardate',
           'lunardate', 'getganzistr', 'strftime']

from datetime import date, timedelta
import locale, time

###################################################################################
## Lunisolar Calendar Table

_BASEYEAR = 1881
_MINDATE = 686686 # 1881.1.30 (lunar 1881.1.1)
_MAXDATE = 748788 # 2051.2.10 (lunar 2050.12.29)
try:
    _DEFAULTLOCALE = locale.getdefaultlocale()[0].split('_')[0]
except:
    _DEFAULTLOCALE = ('koKR', 'utf-8')
    
try: import re; _STRFTIMEREGEXP = re.compile('(?<!%)((?:%%)*)%L(.)')
except ImportError: _STRFTIMEREGEXP = None

_MONTHTABLE = u"\0\u001D\u003B\u0058\u0076\u0093\u00B1\u00CF\u00EC\u010A\u0128\
\u0145\u0163\u0180\u019D\u01BB\u01D8\u01F6\u0213\u0231\u024E\u026C\u028A\u02A7\
\u02C5\u02E3\u0300\u031D\u033B\u0358\u0375\u0393\u03B0\u03CE\u03EC\u040A\u0427\
\u0445\u0463\u0480\u049D\u04BB\u04D8\u04F5\u0513\u0530\u054E\u056C\u0589\u05A7\
\u05C5\u05E3\u0600\u061D\u063B\u0658\u0675\u0693\u06B0\u06CE\u06EB\u0709\u0727\
\u0745\u0762\u0780\u079D\u07BB\u07D8\u07F5\u0813\u0830\u084E\u086B\u0889\u08A7\
\u08C5\u08E2\u0900\u091D\u093B\u0958\u0975\u0993\u09B0\u09CE\u09EB\u0A09\u0A27\
\u0A44\u0A62\u0A80\u0A9D\u0ABB\u0AD8\u0AF5\u0B13\u0B30\u0B4E\u0B6B\u0B89\u0BA6\
\u0BC4\u0BE2\u0BFF\u0C1D\u0C3A\u0C58\u0C75\u0C93\u0CB0\u0CCE\u0CEB\u0D09\u0D26\
\u0D44\u0D61\u0D7F\u0D9D\u0DBA\u0DD8\u0DF5\u0E13\u0E30\u0E4E\u0E6B\u0E89\u0EA6\
\u0EC4\u0EE1\u0EFF\u0F1C\u0F3A\u0F58\u0F75\u0F93\u0FB1\u0FCE\u0FEB\u1009\u1026\
\u1043\u1061\u107E\u109C\u10BA\u10D7\u10F5\u1113\u1131\u114E\u116B\u1189\u11A6\
\u11C3\u11E1\u11FE\u121C\u1239\u1257\u1275\u1293\u12B0\u12CE\u12EB\u1309\u1326\
\u1343\u1361\u137E\u139C\u13B9\u13D7\u13F5\u1413\u1430\u144E\u146B\u1489\u14A6\
\u14C3\u14E1\u14FE\u151C\u1539\u1557\u1574\u1592\u15B0\u15CE\u15EB\u1609\u1626\
\u1643\u1661\u167E\u169C\u16B9\u16D7\u16F4\u1712\u1730\u174D\u176B\u1788\u17A6\
\u17C3\u17E1\u17FE\u181C\u1839\u1857\u1874\u1892\u18AF\u18CD\u18EB\u1908\u1926\
\u1943\u1961\u197E\u199C\u19B9\u19D7\u19F4\u1A12\u1A2F\u1A4D\u1A6A\u1A88\u1AA6\
\u1AC3\u1AE1\u1AFE\u1B1C\u1B39\u1B57\u1B74\u1B91\u1BAF\u1BCC\u1BEA\u1C08\u1C25\
\u1C43\u1C61\u1C7E\u1C9C\u1CB9\u1CD7\u1CF4\u1D11\u1D2F\u1D4C\u1D6A\u1D87\u1DA5\
\u1DC3\u1DE1\u1DFE\u1E1C\u1E39\u1E57\u1E74\u1E91\u1EAF\u1ECC\u1EEA\u1F07\u1F25\
\u1F43\u1F61\u1F7E\u1F9C\u1FB9\u1FD7\u1FF4\u2011\u202F\u204C\u2069\u2087\u20A5\
\u20C2\u20E0\u20FE\u211C\u2139\u2157\u2174\u2191\u21AF\u21CC\u21E9\u2207\u2225\
\u2242\u2260\u227E\u229B\u22B9\u22D7\u22F4\u2311\u232F\u234C\u236A\u2387\u23A5\
\u23C2\u23E0\u23FE\u241B\u2439\u2456\u2474\u2491\u24AF\u24CC\u24EA\u2507\u2525\
\u2542\u2560\u257D\u259B\u25B8\u25D6\u25F4\u2611\u262F\u264C\u266A\u2687\u26A5\
\u26C2\u26DF\u26FD\u271B\u2738\u2756\u2773\u2791\u27AF\u27CC\u27EA\u2807\u2825\
\u2842\u285F\u287D\u289A\u28B8\u28D5\u28F3\u2911\u292F\u294C\u296A\u2987\u29A5\
\u29C2\u29DF\u29FD\u2A1A\u2A38\u2A55\u2A73\u2A91\u2AAF\u2ACC\u2AEA\u2B07\u2B25\
\u2B42\u2B5F\u2B7D\u2B9A\u2BB7\u2BD5\u2BF3\u2C10\u2C2E\u2C4C\u2C6A\u2C87\u2CA5\
\u2CC2\u2CDF\u2CFD\u2D1A\u2D37\u2D55\u2D73\u2D90\u2DAE\u2DCC\u2DEA\u2E07\u2E25\
\u2E42\u2E5F\u2E7D\u2E9A\u2EB7\u2ED5\u2EF2\u2F10\u2F2E\u2F4C\u2F69\u2F87\u2FA5\
\u2FC2\u2FDF\u2FFD\u301A\u3038\u3055\u3072\u3090\u30AE\u30CB\u30E9\u3107\u3124\
\u3142\u315F\u317D\u319A\u31B8\u31D5\u31F3\u3210\u322E\u324B\u3269\u3286\u32A4\
\u32C2\u32DF\u32FD\u331A\u3338\u3355\u3373\u3390\u33AD\u33CB\u33E8\u3406\u3424\
\u3441\u345F\u347D\u349A\u34B8\u34D5\u34F3\u3510\u352D\u354B\u3568\u3586\u35A3\
\u35C1\u35DF\u35FD\u361A\u3638\u3655\u3673\u3690\u36AD\u36CB\u36E8\u3706\u3723\
\u3741\u375F\u377C\u379A\u37B8\u37D5\u37F3\u3810\u382D\u384B\u3868\u3885\u38A3\
\u38C1\u38DE\u38FC\u391A\u3938\u3955\u3973\u3990\u39AD\u39CB\u39E8\u3A05\u3A23\
\u3A40\u3A5E\u3A7C\u3A9A\u3AB7\u3AD5\u3AF3\u3B10\u3B2D\u3B4B\u3B68\u3B85\u3BA3\
\u3BC0\u3BDE\u3BFC\u3C19\u3C37\u3C55\u3C72\u3C90\u3CAD\u3CCB\u3CE8\u3D06\u3D23\
\u3D40\u3D5E\u3D7C\u3D99\u3DB7\u3DD4\u3DF2\u3E10\u3E2D\u3E4B\u3E68\u3E86\u3EA3\
\u3EC0\u3EDE\u3EFB\u3F19\u3F37\u3F54\u3F72\u3F8F\u3FAD\u3FCB\u3FE8\u4006\u4023\
\u4041\u405E\u407B\u4099\u40B6\u40D4\u40F1\u410F\u412D\u414A\u4168\u4186\u41A3\
\u41C1\u41DE\u41FB\u4219\u4236\u4254\u4271\u428F\u42AD\u42CA\u42E8\u4306\u4323\
\u4341\u435E\u437B\u4399\u43B6\u43D3\u43F1\u440F\u442C\u444A\u4468\u4486\u44A3\
\u44C1\u44DE\u44FB\u4519\u4536\u4553\u4571\u458E\u45AC\u45CA\u45E8\u4605\u4623\
\u4641\u465E\u467B\u4699\u46B6\u46D3\u46F1\u470E\u472C\u474A\u4767\u4785\u47A3\
\u47C1\u47DE\u47FB\u4819\u4836\u4853\u4871\u488E\u48AC\u48C9\u48E7\u4905\u4923\
\u4940\u495E\u497B\u4999\u49B6\u49D3\u49F1\u4A0E\u4A2C\u4A49\u4A67\u4A85\u4AA2\
\u4AC0\u4ADE\u4AFB\u4B19\u4B36\u4B54\u4B71\u4B8E\u4BAC\u4BC9\u4BE7\u4C04\u4C22\
\u4C40\u4C5D\u4C7B\u4C99\u4CB6\u4CD4\u4CF1\u4D0F\u4D2C\u4D49\u4D67\u4D84\u4DA2\
\u4DBF\u4DDD\u4DFB\u4E18\u4E36\u4E54\u4E71\u4E8F\u4EAC\u4EC9\u4EE7\u4F04\u4F22\
\u4F3F\u4F5D\u4F7A\u4F98\u4FB6\u4FD4\u4FF1\u500F\u502C\u5049\u5067\u5084\u50A1\
\u50BF\u50DC\u50FA\u5118\u5136\u5153\u5171\u518F\u51AC\u51C9\u51E7\u5204\u5221\
\u523F\u525C\u527A\u5298\u52B5\u52D3\u52F1\u530F\u532C\u5349\u5367\u5384\u53A1\
\u53BF\u53DC\u53FA\u5417\u5435\u5453\u5471\u548E\u54AC\u54C9\u54E7\u5504\u5521\
\u553F\u555C\u557A\u5597\u55B5\u55D3\u55F0\u560E\u562C\u5649\u5667\u5684\u56A1\
\u56BF\u56DC\u56FA\u5717\u5735\u5752\u5770\u578E\u57AB\u57C9\u57E7\u5804\u5822\
\u583F\u585C\u587A\u5897\u58B5\u58D2\u58F0\u590D\u592B\u5949\u5966\u5984\u59A2\
\u59BF\u59DD\u59FA\u5A17\u5A35\u5A52\u5A70\u5A8D\u5AAB\u5AC8\u5AE6\u5B04\u5B21\
\u5B3F\u5B5D\u5B7A\u5B97\u5BB5\u5BD2\u5BEF\u5C0D\u5C2A\u5C48\u5C66\u5C84\u5CA1\
\u5CBF\u5CDD\u5CFA\u5D17\u5D35\u5D52\u5D6F\u5D8D\u5DAA\u5DC8\u5DE6\u5E03\u5E21\
\u5E3F\u5E5D\u5E7A\u5E97\u5EB5\u5ED2\u5EEF\u5F0D\u5F2A\u5F48\u5F65\u5F83\u5FA1\
\u5FBF\u5FDC\u5FFA\u6017\u6035\u6052\u606F\u608D\u60AA\u60C8\u60E5\u6103\u6121\
\u613F\u615C\u617A\u6197\u61B5\u61D2\u61EF\u620D\u622A\u6248\u6265\u6283\u62A1\
\u62BE\u62DC\u62FA\u6317\u6335\u6352\u636F\u638D\u63AA\u63C8\u63E5\u6403\u6420\
\u643E\u645C\u6479\u6497\u64B4\u64D2\u64EF\u650D\u652A\u6548\u6565\u6583\u65A0\
\u65BE\u65DB\u65F9\u6617\u6634\u6652\u666F\u668D\u66AA\u66C8\u66E5\u6703\u6720\
\u673D\u675B\u6779\u6796\u67B4\u67D2\u67EF\u680D\u682B\u6848\u6865\u6883\u68A0\
\u68BD\u68DB\u68F8\u6916\u6934\u6951\u696F\u698D\u69AB\u69C8\u69E5\u6A03\u6A20\
\u6A3D\u6A5B\u6A78\u6A96\u6AB3\u6AD1\u6AEF\u6B0D\u6B2A\u6B48\u6B65\u6B83\u6BA0\
\u6BBD\u6BDB\u6BF8\u6C16\u6C33\u6C51\u6C6F\u6C8D\u6CAA\u6CC8\u6CE5\u6D03\u6D20\
\u6D3D\u6D5B\u6D78\u6D96\u6DB3\u6DD1\u6DEF\u6E0C\u6E2A\u6E48\u6E65\u6E83\u6EA0\
\u6EBD\u6EDB\u6EF8\u6F16\u6F33\u6F51\u6F6E\u6F8C\u6FAA\u6FC7\u6FE5\u7002\u7020\
\u703D\u705B\u7078\u7096\u70B3\u70D1\u70EE\u710C\u7129\u7147\u7165\u7182\u71A0\
\u71BD\u71DB\u71F8\u7216\u7233\u7251\u726E\u728C\u72A9\u72C7\u72E4\u7302\u7320\
\u733D\u735B\u7378\u7396\u73B3\u73D1\u73EE\u740B\u7429\u7446\u7464\u7482\u749F\
\u74BD\u74DB\u74F8\u7516\u7533\u7551\u756E\u758B\u75A9\u75C6\u75E4\u7601\u761F\
\u763D\u765B\u7678\u7696\u76B3\u76D1\u76EE\u770B\u7729\u7746\u7764\u7781\u779F\
\u77BD\u77DB\u77F8\u7816\u7833\u7851\u786E\u788B\u78A9\u78C6\u78E3\u7901\u791F\
\u793D\u795A\u7978\u7996\u79B3\u79D1\u79EE\u7A0B\u7A29\u7A46\u7A63\u7A81\u7A9F\
\u7ABC\u7ADA\u7AF8\u7B15\u7B33\u7B51\u7B6E\u7B8B\u7BA9\u7BC6\u7BE4\u7C01\u7C1F\
\u7C3C\u7C5A\u7C78\u7C95\u7CB3\u7CD0\u7CEE\u7D0B\u7D29\u7D46\u7D64\u7D81\u7D9F\
\u7DBC\u7DDA\u7DF7\u7E15\u7E32\u7E50\u7E6E\u7E8B\u7EA9\u7EC6\u7EE4\u7F01\u7F1F\
\u7F3C\u7F59\u7F77\u7F95\u7FB2\u7FD0\u7FED\u800B\u8029\u8046\u8064\u8081\u809F\
\u80BC\u80D9\u80F7\u8114\u8132\u814F\u816D\u818B\u81A9\u81C6\u81E4\u8201\u821F\
\u823C\u8259\u8277\u8294\u82B2\u82CF\u82ED\u830B\u8329\u8346\u8364\u8381\u839F\
\u83BC\u83D9\u83F7\u8414\u8431\u844F\u846D\u848B\u84A8\u84C6\u84E4\u8501\u851F\
\u853C\u8559\u8577\u8594\u85B1\u85CF\u85ED\u860A\u8628\u8646\u8664\u8681\u869F\
\u86BC\u86D9\u86F7\u8714\u8731\u874F\u876C\u878A\u87A8\u87C6\u87E3\u8801\u881E\
\u883C\u8859\u8877\u8894\u88B2\u88CF\u88EC\u890A\u8928\u8945\u8963\u8981\u899E\
\u89BC\u89D9\u89F7\u8A14\u8A32\u8A4F\u8A6C\u8A8A\u8AA8\u8AC5\u8AE3\u8B00\u8B1E\
\u8B3C\u8B59\u8B77\u8B94\u8BB2\u8BCF\u8BED\u8C0A\u8C27\u8C45\u8C62\u8C80\u8C9E\
\u8CBB\u8CD9\u8CF7\u8D14\u8D32\u8D4F\u8D6D\u8D8A\u8DA7\u8DC5\u8DE2\u8E00\u8E1D\
\u8E3B\u8E59\u8E76\u8E94\u8EB2\u8ECF\u8EED\u8F0A\u8F27\u8F45\u8F62\u8F7F\u8F9D\
\u8FBB\u8FD8\u8FF6\u9014\u9032\u904F\u906D\u908A\u90A7\u90C5\u90E2\u90FF\u911D\
\u913B\u9158\u9176\u9194\u91B2\u91CF\u91ED\u920A\u9227\u9245\u9262\u927F\u929D\
\u92BA\u92D8\u92F6\u9314\u9331\u934F\u936D\u938A\u93A7\u93C5\u93E2\u93FF\u941D\
\u943A\u9458\u9476\u9493\u94B1\u94CF\u94EC\u950A\u9527\u9545\u9562\u957F\u959D\
\u95BA\u95D8\u95F5\u9613\u9631\u964E\u966C\u968A\u96A7\u96C5\u96E2\u9700\u971D\
\u973A\u9758\u9775\u9793\u97B1\u97CE\u97EC\u9809\u9827\u9845\u9862\u9880\u989D\
\u98BB\u98D8\u98F5\u9913\u9930\u994E\u996B\u9989\u99A7\u99C4\u99E2\u9A00\u9A1D\
\u9A3B\u9A58\u9A75\u9A93\u9AB0\u9ACE\u9AEB\u9B09\u9B27\u9B44\u9B62\u9B80\u9B9D\
\u9BBB\u9BD8\u9BF5\u9C13\u9C30\u9C4D\u9C6B\u9C89\u9CA6\u9CC4\u9CE2\u9D00\u9D1D\
\u9D3B\u9D58\u9D75\u9D93\u9DB0\u9DCD\u9DEB\u9E08\u9E26\u9E44\u9E62\u9E7F\u9E9D\
\u9EBB\u9ED8\u9EF5\u9F13\u9F30\u9F4D\u9F6B\u9F88\u9FA6\u9FC4\u9FE1\u9FFF\uA01D\
\uA03A\uA058\uA075\uA093\uA0B0\uA0CD\uA0EB\uA108\uA126\uA143\uA161\uA17F\uA19D\
\uA1BA\uA1D8\uA1F5\uA213\uA230\uA24D\uA26B\uA288\uA2A6\uA2C3\uA2E1\uA2FF\uA31C\
\uA33A\uA358\uA375\uA393\uA3B0\uA3CE\uA3EB\uA408\uA426\uA443\uA461\uA47E\uA49C\
\uA4BA\uA4D7\uA4F5\uA512\uA530\uA54E\uA56B\uA589\uA5A6\uA5C3\uA5E1\uA5FE\uA61C\
\uA639\uA657\uA675\uA692\uA6B0\uA6CE\uA6EB\uA709\uA726\uA743\uA761\uA77E\uA79B\
\uA7B9\uA7D7\uA7F4\uA812\uA830\uA84E\uA86B\uA889\uA8A6\uA8C3\uA8E1\uA8FE\uA91B\
\uA939\uA956\uA974\uA992\uA9B0\uA9CD\uA9EB\uAA09\uAA26\uAA43\uAA61\uAA7E\uAA9B\
\uAAB9\uAAD6\uAAF4\uAB12\uAB2F\uAB4D\uAB6B\uAB89\uABA6\uABC3\uABE1\uABFE\uAC1B\
\uAC39\uAC56\uAC74\uAC91\uACAF\uACCD\uACEB\uAD08\uAD26\uAD43\uAD61\uAD7E\uAD9B\
\uADB9\uADD6\uADF4\uAE11\uAE2F\uAE4D\uAE6A\uAE88\uAEA6\uAEC3\uAEE1\uAEFE\uAF1B\
\uAF39\uAF56\uAF74\uAF91\uAFAF\uAFCC\uAFEA\uB008\uB025\uB043\uB060\uB07E\uB09B\
\uB0B9\uB0D6\uB0F4\uB111\uB12F\uB14C\uB16A\uB187\uB1A5\uB1C3\uB1E0\uB1FE\uB21C\
\uB239\uB256\uB274\uB291\uB2AF\uB2CC\uB2EA\uB307\uB325\uB342\uB360\uB37E\uB39B\
\uB3B9\uB3D7\uB3F4\uB411\uB42F\uB44C\uB469\uB487\uB4A4\uB4C2\uB4E0\uB4FE\uB51B\
\uB539\uB557\uB574\uB591\uB5AF\uB5CC\uB5E9\uB607\uB624\uB642\uB660\uB67D\uB69B\
\uB6B9\uB6D7\uB6F4\uB711\uB72F\uB74C\uB769\uB787\uB7A4\uB7C2\uB7DF\uB7FD\uB81B\
\uB839\uB856\uB874\uB891\uB8AF\uB8CC\uB8E9\uB907\uB924\uB942\uB95F\uB97D\uB99B\
\uB9B8\uB9D6\uB9F4\uBA11\uBA2F\uBA4C\uBA69\uBA87\uBAA4\uBAC2\uBADF\uBAFD\uBB1A\
\uBB38\uBB56\uBB74\uBB91\uBBAF\uBBCC\uBBE9\uBC07\uBC24\uBC42\uBC5F\uBC7D\uBC9A\
\uBCB8\uBCD6\uBCF3\uBD11\uBD2E\uBD4C\uBD69\uBD87\uBDA4\uBDC2\uBDDF\uBDFD\uBE1A\
\uBE38\uBE55\uBE73\uBE90\uBEAE\uBECC\uBEE9\uBF07\uBF24\uBF42\uBF5F\uBF7D\uBF9A\
\uBFB7\uBFD5\uBFF2\uC010\uC02E\uC04C\uC069\uC087\uC0A4\uC0C2\uC0DF\uC0FD\uC11A\
\uC137\uC155\uC172\uC190\uC1AE\uC1CB\uC1E9\uC207\uC224\uC242\uC25F\uC27D\uC29A\
\uC2B7\uC2D5\uC2F2\uC310\uC32D\uC34B\uC369\uC387\uC3A4\uC3C2\uC3DF\uC3FD\uC41A\
\uC437\uC455\uC472\uC490\uC4AD\uC4CB\uC4E9\uC507\uC524\uC542\uC55F\uC57D\uC59A\
\uC5B7\uC5D5\uC5F2\uC610\uC62D\uC64B\uC669\uC686\uC6A4\uC6C2\uC6DF\uC6FD\uC71A\
\uC737\uC755\uC772\uC790\uC7AD\uC7CB\uC7E8\uC806\uC824\uC841\uC85F\uC87C\uC89A\
\uC8B7\uC8D5\uC8F2\uC910\uC92D\uC94B\uC968\uC986\uC9A3\uC9C1\uC9DF\uC9FC\uCA1A\
\uCA37\uCA55\uCA72\uCA90\uCAAD\uCACB\uCAE8\uCB06\uCB23\uCB41\uCB5E\uCB7C\uCB9A\
\uCBB7\uCBD5\uCBF2\uCC10\uCC2D\uCC4B\uCC68\uCC85\uCCA3\uCCC0\uCCDE\uCCFC\uCD19\
\uCD37\uCD55\uCD72\uCD90\uCDAD\uCDCB\uCDE8\uCE05\uCE23\uCE40\uCE5E\uCE7B\uCE99\
\uCEB7\uCED5\uCEF2\uCF10\uCF2D\uCF4B\uCF68\uCF85\uCFA3\uCFC0\uCFDE\uCFFB\uD019\
\uD037\uD055\uD072\uD090\uD0AD\uD0CB\uD0E8\uD105\uD123\uD140\uD15D\uD17B\uD199\
\uD1B7\uD1D4\uD1F2\uD210\uD22D\uD24B\uD268\uD285\uD2A3\uD2C0\uD2DD\uD2FB\uD319\
\uD336\uD354\uD372\uD38F\uD3AD\uD3CB\uD3E8\uD405\uD423\uD440\uD45D\uD47B\uD499\
\uD4B6\uD4D4\uD4F1\uD50F\uD52D\uD54A\uD568\uD585\uD5A3\uD5C0\uD5DE\uD5FB\uD619\
\uD636\uD654\uD671\uD68F\uD6AC\uD6CA\uD6E8\uD705\uD723\uD740\uD75E\uD77B\uD799\
\uD7B6\uD7D3\uD7F1\uD80E\uD82C\uD84A\uD867\uD885\uD8A3\uD8C0\uD8DE\uD8FB\uD919\
\uD936\uD953\uD971\uD98E\uD9AC\uD9C9\uD9E7\uDA05\uDA23\uDA40\uDA5E\uDA7B\uDA99\
\uDAB6\uDAD3\uDAF1\uDB0E\uDB2C\uDB49\uDB67\uDB85\uDBA3\uDBC0\uDBDE\uDBFB\uDC19\
\uDC36\uDC53\uDC71\uDC8E\uDCAB\uDCC9\uDCE7\uDD04\uDD22\uDD40\uDD5E\uDD7B\uDD99\
\uDDB6\uDDD3\uDDF1\uDE0E\uDE2B\uDE49\uDE67\uDE84\uDEA2\uDEC0\uDEDE\uDEFB\uDF19\
\uDF36\uDF53\uDF71\uDF8E\uDFAB\uDFC9\uDFE6\uE004\uE022\uE040\uE05D\uE07B\uE098\
\uE0B6\uE0D3\uE0F1\uE10E\uE12B\uE149\uE166\uE184\uE1A2\uE1BF\uE1DD\uE1FB\uE218\
\uE236\uE253\uE271\uE28E\uE2AC\uE2C9\uE2E6\uE304\uE321\uE33F\uE35D\uE37A\uE398\
\uE3B6\uE3D3\uE3F1\uE40E\uE42C\uE449\uE467\uE484\uE4A1\uE4BF\uE4DC\uE4FA\uE518\
\uE535\uE553\uE571\uE58E\uE5AC\uE5C9\uE5E7\uE604\uE621\uE63F\uE65C\uE67A\uE697\
\uE6B5\uE6D3\uE6F0\uE70E\uE72C\uE749\uE767\uE784\uE7A1\uE7BF\uE7DC\uE7F9\uE817\
\uE835\uE852\uE870\uE88E\uE8AC\uE8C9\uE8E7\uE904\uE921\uE93F\uE95C\uE979\uE997\
\uE9B4\uE9D2\uE9F0\uEA0E\uEA2C\uEA49\uEA67\uEA84\uEAA1\uEABF\uEADC\uEAF9\uEB17\
\uEB34\uEB52\uEB70\uEB8E\uEBAB\uEBC9\uEBE7\uEC04\uEC21\uEC3F\uEC5C\uEC79\uEC97\
\uECB4\uECD2\uECF0\uED0D\uED2B\uED49\uED66\uED84\uEDA1\uEDBF\uEDDC\uEDF9\uEE17\
\uEE34\uEE52\uEE6F\uEE8D\uEEAB\uEEC8\uEEE6\uEF04\uEF21\uEF3F\uEF5C\uEF7A\uEF97\
\uEFB4\uEFD2\uEFEF\uF00D\uF02A\uF048\uF066\uF083\uF0A1\uF0BF\uF0DC\uF0FA\uF117\
\uF135\uF152\uF16F\uF18D\uF1AA\uF1C8\uF1E5\uF203\uF221\uF23E\uF25C\uF27A\uF297"

_YEARTABLE = u"\00\u000D\u0019\u0025\u0032\u003E\u004A\u0057\u0063\u006F\u007C\
\u0088\u0095\u00A1\u00AD\u00BA\u00C6\u00D2\u00DF\u00EB\u00F8\u0104\u0110\u011D\
\u0129\u0135\u0142\u014E\u015A\u0167\u0173\u0180\u018C\u0198\u01A5\u01B1\u01BD\
\u01CA\u01D6\u01E3\u01EF\u01FB\u0208\u0214\u0220\u022D\u0239\u0245\u0252\u025E\
\u026B\u0277\u0283\u0290\u029C\u02A8\u02B5\u02C1\u02CE\u02DA\u02E6\u02F3\u02FF\
\u030B\u0318\u0324\u0330\u033D\u0349\u0356\u0362\u036E\u037B\u0387\u0393\u03A0\
\u03AC\u03B9\u03C5\u03D1\u03DE\u03EA\u03F6\u0403\u040F\u041B\u0428\u0434\u0441\
\u044D\u0459\u0466\u0472\u047E\u048B\u0497\u04A4\u04B0\u04BC\u04C9\u04D5\u04E1\
\u04EE\u04FA\u0507\u0513\u051F\u052C\u0538\u0544\u0551\u055D\u0569\u0576\u0582\
\u058F\u059B\u05A7\u05B4\u05C0\u05CC\u05D9\u05E5\u05F1\u05FE\u060A\u0617\u0623\
\u062F\u063C\u0648\u0654\u0661\u066D\u067A\u0686\u0692\u069F\u06AB\u06B7\u06C4\
\u06D0\u06DC\u06E9\u06F5\u0702\u070E\u071A\u0727\u0733\u073F\u074C\u0758\u0765\
\u0771\u077D\u078A\u0796\u07A2\u07AF\u07BB\u07C7\u07D4\u07E0\u07ED\u07F9\u0805\
\u0812\u081E\u082A"

_LEAPTABLE = "\7\0\0\5\0\0\4\0\0\2\0\6\0\0\5\0\0\3\0\10\0\0\5\0\0\4\0\0\2\0\6\
\0\0\5\0\0\2\0\7\0\0\5\0\0\4\0\0\2\0\6\0\0\5\0\0\3\0\7\0\0\6\0\0\4\0\0\2\0\7\0\
\0\5\0\0\3\0\10\0\0\6\0\0\4\0\0\3\0\7\0\0\5\0\0\4\0\10\0\0\6\0\0\4\0\12\0\0\6\
\0\0\5\0\0\3\0\10\0\0\5\0\0\4\0\0\2\0\7\0\0\5\0\0\3\0\11\0\0\5\0\0\4\0\0\2\0\6\
\0\0\5\0\0\3\0\13\0\0\6\0\0\5\0\0\2\0\7\0\0\5\0\0\3"

_GANZIMAP = {
    'ko': u'\uac11\uc744\ubcd1\uc815\ubb34\uae30\uacbd\uc2e0\uc784\uacc4\uc790'
          u'\ucd95\uc778\ubb18\uc9c4\uc0ac\uc624\ubbf8\uc2e0\uc720\uc220\ud574',
    'ja': u'\u7532\u4e59\u4e19\u4e01\u620a\u5df1\u5e9a\u8f9b\u58ec\u7678\u5b50'
          u'\u4e11\u5bc5\u536f\u8fb0\u5df3\u5348\u672a\u7533\u9149\u620c\u4ea5',
    'zh': u'\u7532\u4e59\u4e19\u4e01\u620a\u5df1\u5e9a\u8f9b\u58ec\u7678\u5b50'
          u'\u4e11\u5bc5\u536f\u8fb0\u5df3\u5348\u672a\u7533\u9149\u620c\u4ea5',
}

###################################################################################
## Basic Functions

def _bisect(a, x):
    lo = 0; hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x < ord(a[mid]): hi = mid
        else: lo = mid + 1
    return lo - 1

def sol2lun(year, month, day, leap=False):
    """sol2lun(year, month, day, leap=False) -> (year, month, day, leap)
    Returns corresponding date in lunar calendar. leap will be ignored."""
    days = date(year, month, day).toordinal()
    if not _MINDATE <= days <= _MAXDATE:
        raise ValueError, "year is out of range"
    days -= _MINDATE
    month = _bisect(_MONTHTABLE, days)
    year = _bisect(_YEARTABLE, month)
    month, day = month - ord(_YEARTABLE[year]) + 1, days - ord(_MONTHTABLE[month]) + 1
    if (ord(_LEAPTABLE[year]) or 13) < month:
        month -= 1
        leap = (ord(_LEAPTABLE[year]) == month)
    else:
        leap = False
    return (year + _BASEYEAR, month, day, leap)

def lun2sol(year, month, day, leap=False):
    """lun2sol(year, month, day, leap=False) -> (year, month, day, leap)
    Returns corresponding date in solar calendar."""
    year -= _BASEYEAR
    if not 0 <= year < len(_YEARTABLE):
        raise ValueError, "year is out of range"
    if not 1 <= month <= 12:
        raise ValueError, "wrong month"
    if leap and ord(_LEAPTABLE[year]) != month:
        raise ValueError, "wrong leap month"
    months = ord(_YEARTABLE[year]) + month - 1
    if leap or (ord(_LEAPTABLE[year]) or 13) < month:
        months += 1
    days = ord(_MONTHTABLE[months]) + day - 1
    if day < 1 or days >= ord(_MONTHTABLE[months + 1]):
        raise ValueError, "wrong day"
    return date.fromordinal(days + _MINDATE).timetuple()[:3] + (False,)

def getganzistr(index, locale=None):
    """getganzistr(index, locale=None) -> unicode string
    Returns corresponding unicode string of ganzi.
    locale can be "ko", "ja", "zh". Uses default locale when locale is ignored."""
    locale = locale or _DEFAULTLOCALE
    return _GANZIMAP[locale][index%10] + _GANZIMAP[locale][10+index%12]

def strftime(format, t=None):
    """strftime(format, t=None) -> string
    Returns formatted string of given timestamp. If timestamp is omitted,
    current timestamp (return value of time.localtime()) is used.

    Similar to time.strftime, but has the following extensions:
      %LC - (year / 100) as a decimal number (at least 2 digits)
      %Ld - lunar day of the month as a decimal number [01,30]
      %Le - same as %Ld, but preceding blank instead of zero
      %LF - same as "%LY-%Lm-%Ld"
      %Lj - day of the lunar year as a decimal number [001,390]
      %Ll - 0 for non-leap month, 1 for leap month
      %Lm - lunar month as a decimal number [01,12]
      %Ly - lunar year without century as a decimal number [00,99]
      %LY - lunar year with century as a decimal number
    """
    if t is None: t = time.localtime()
    if _STRFTIMEREGEXP is not None:
        lt = sol2lun(*t[:3])
        lord = date(t[0], t[1], t[2]).toordinal() - _MINDATE
        ldoy = lord - ord(_MONTHTABLE[ord(_YEARTABLE[lt[0] - _BASEYEAR])]) + 1
        lmap = {'Y': '%04d' % lt[0], 'm': '%02d' % lt[1], 'd': '%02d' % lt[2],
                'y': '%02d' % (lt[0] % 100), 'C': '%02d' % (lt[0] // 100),
                'F': '%04d-%02d-%02d' % lt[:3], 'e': str(lt[2]),
                'l': '%d' % lt[3], 'j': '%03d' % ldoy}
        format = _STRFTIMEREGEXP.sub(lambda m: '%' * (len(m.group(1)) / 2) +
                                               lmap.get(m.group(2), ''), format)
    return time.strftime(format, t)

###################################################################################
## Class Declaration

# just alias. we have lunardate, so why not we have solardate?
solardate = date

class lunardate(date):
    """lunardate(year, month, day, leap=False) -> new lunardate object"""

    def __new__(cls, year, month, day, leap=False):
        obj = date.__new__(cls, *lun2sol(year, month, day, leap)[:3])
        object.__setattr__(obj, 'lunaryear', year)
        object.__setattr__(obj, 'lunarmonth', month)
        object.__setattr__(obj, 'lunarday', day)
        object.__setattr__(obj, 'lunarleap', leap)
        return obj
    
    def __repr__(self):
        return '%s.%s(%d, %d, %d, %s)' % \
               (self.__class__.__module__, self.__class__.__name__,
                self.lunaryear, self.lunarmonth, self.lunarday, self.lunarleap)
    
    min = type('propertyproxy', (object,), {
        '__doc__': 'lunardate.min -> The earliest representable date',
        '__get__': lambda self, inst, cls: cls.fromordinal(_MINDATE)})()
    max = type('propertyproxy', (object,), {
        '__doc__': 'lunardate.max -> The latest representable date',
        '__get__': lambda self, inst, cls: cls.fromordinal(_MAXDATE)})()
    
    def __setattr__(self, name, value):
        raise AttributeError, "can't set attribute."
    
    def __add__(self, other):
        return self.fromsolardate(date.__add__(self, other))
    
    def __radd__(self, other):
        return self.fromsolardate(date.__radd__(self, other))
    
    def __sub__(self, other):
        result = date.__sub__(self, other)
        if not isinstance(result, timedelta):
            result = self.fromsolardate(result)
        return result

    def replace(self, year=None, month=None, day=None, leap=None):
        """lunardate.replace(year, month, day, leap) -> new lunardate object
        Same as date.replace, but returns lunardate object instead of date object."""
        if leap is None: leap = self.lunarleap
        return self.__class__(year or self.lunaryear, month or self.lunarmonth,
                              day or self.month, leap)
    
    def tosolardate(self):
        """lunardate.tosolardate() -> date object
        Returns corresponding date object."""
        return date(self.year, self.month, self.day)
    
    def today(self):
        """lunardate.today() -> new lunardate object
        Returns lunardate object which represents today."""
        return self.fromsolardate(date.today())
    
    def fromsolardate(self, solardate):
        """lunardate.fromsolardate(solardate) -> new lunardate object
        Returns corresponding lunardate object from date object."""
        return self(*sol2lun(*solardate.timetuple()[:3]))
    
    def fromtimestamp(self, timestamp):
        """lunardate.fromtimestamp(timestamp) -> new lunardate object
        Returns corresponding lunardate object from UNIX timestamp."""
        return self.fromsolardate(date.fromtimestamp(timestamp))
    
    def fromordinal(self, ordinal):
        """lunardate.fromordinal(ordinal) -> new lunardate object
        Returns corresponding lunardate object from Gregorian ordinal."""
        return self.fromsolardate(date.fromordinal(ordinal))
    
    def getganzi(self):
        """lunardate.getganzi() -> (year_ganzi, month_ganzi, day_ganzi)
        Returns ganzi index between 0..59 from lunardate object.
        Ganzi index can be converted using getganzistr function."""
        return ((self.lunaryear + 56) % 60,
                (self.lunaryear * 12 + self.lunarmonth + 13) % 60,
                (self.toordinal() + 14) % 60)

    def getganzistr(self, locale=None):
        """lunardate.getganzistr(locale=None) -> 3-tuple of unicode string
        Returns unicode string of ganzi from lunardate object.
        See getganzistr global function for detail."""
        return tuple([getganzistr(i, locale) for i in self.getganzi()])

    def strftime(self, format):
        """lunardate.strftime(format) -> string
        Returns formatted string of lunardate object.
        See strftime global function for detail."""
        return strftime(format, self.timetuple())
    
    today = classmethod(today)
    fromsolardate = classmethod(fromsolardate)
    fromtimestamp = classmethod(fromtimestamp)
    fromordinal = classmethod(fromordinal)

# we create new lunardate class from old lunardate class using typeproxy,
# because default type class always allows setting class variable.
# __slots__ is added later to forbid descriptor initialization by type.
class typeproxy(type):
    def __setattr__(self, name, value):
        raise AttributeError, "can't set attribute."
clsdict = dict(lunardate.__dict__)
clsdict['__slots__'] = ['lunaryear', 'lunarmonth', 'lunarday', 'lunarleap']
lunardate = typeproxy(lunardate.__name__, lunardate.__bases__, clsdict)
del typeproxy

###################################################################################
## Command Line Interface

if __name__ == '__main__':
    import sys
    try:
        mode = sys.argv[1].lower()
        if mode == 'today':
            if len(sys.argv) != 2: raise RuntimeError
            today = lunardate.today()
            isleap = today.lunarleap and ' (leap)' or ''
            print today.strftime('Today: solar %Y-%m-%d %a = lunar %LY-%Lm-%Ld' + isleap)
        elif mode == 'solar':
            if len(sys.argv) != 5: raise RuntimeError
            solar = lunardate.fromsolardate(date(*map(int, sys.argv[2:])))
            isleap = solar.lunarleap and ' (leap)' or ''
            print solar.strftime('solar %Y-%m-%d %a -> lunar %LY-%Lm-%Ld' + isleap)
        elif mode == 'lunar':
            if len(sys.argv) not in (5, 6): raise RuntimeError
            leap = (len(sys.argv) == 6 and sys.argv[5].lower() == 'leap')
            solar = lunardate(*(map(int, sys.argv[2:5]) + [leap]))
            isleap = leap and ' (leap)' or ''
            print solar.strftime('lunar %LY-%Lm-%Ld' + isleap + ' -> solar %Y-%m-%d %a')
        else:
            raise RuntimeError
    except (IndexError, RuntimeError):
        app = sys.argv[0]
        print 'Usage:'
        print '  for today - python %s today' % app
        print '  for solar to lunar - python %s solar <year> <month> <day>' % app
        print '  for lunar to solar - python %s lunar <year> <month> <day> [leap]' % app
    except:
        print 'Error: %s' % sys.exc_info()[1]

