import numpy
class PowerSpectrum(object):
    """ A normalized powerspectrum for give sigma8,
        k, p are in Mpc/h units 
    """
    def __init__(self, k, p, sigma8=None):
        self.logK = numpy.log10(k)
        self.logP = numpy.log10(p)

        self.Norm = 1.0
        if sigma8 is not None:
            self.Norm = sigma8 ** 2 / self.sigma_squared_of_R(8.0)
            self.sigma8 = sigma8
        else:
            self.sigma8 = self.sigma_squared_of_R(8.0) ** 0.5
    def PofK(self, k):
        """
        returns power spectrum as a function of wavenumber k
        This is P/(2pi)**3.
        This is NOT P
        """
        logk = numpy.log10(k)
        return self.Norm * 10**(numpy.interp(logk, self.logK, self.logP))

    def WofK(self,x):
        """
        returns W(k*R), which is the fourier transform of the top-hat function.
        """
        #Series expansion actually good until kr~1
        if x < 1e-2:
            return 1./3. - x**2/30. +x**4/840.
        else:
            return 3.0 * (numpy.sin(x) - x*numpy.cos(x)) / x**3

    def sigma_squared_integrand(self, k, R):
        """
        integrand for integral to get sigma^2(R).
        Parameters: Rcom is R in comoving Mpc/h
        """
        f = k**2* self.PofK(k) * \
            4 * numpy.pi *self.WofK(R*k)**2.0 
            #/ (2 * numpy.pi) ** 3
        return f
    def sigma_squared_of_R(self, R):
        """
        /* calculates sigma^2(R). This is the routine where the magic happens (or
        whatever it is that we do here). Integrates the sigma_squared_integrand
        parameter from 0 to infinity.
        Note that R is in h^-1 Mpc (comoving)
        */
        """
        from scipy.integrate import quad

        result = quad(self.sigma_squared_integrand,0,numpy.Inf, epsrel=1e-2,
                args=(R,))[0]
        sigmasquaredofR = result 
        return sigmasquaredofR 

from StringIO import StringIO

_psdata_wmap9 = StringIO("""
-4.000000010971201725e+00 -1.572772979736328125e+00
-3.991314124312373757e+00 -1.564339637756347656e+00
-3.982628201194406525e+00 -1.555906176567077637e+00
-3.973942312383877962e+00 -1.547472834587097168e+00
-3.965256444046747930e+00 -1.539039492607116699e+00
-3.956570535763844987e+00 -1.530606150627136230e+00
-3.947884682697883285e+00 -1.522173643112182617e+00
-3.939198792096135993e+00 -1.513740181922912598e+00
-3.930512872116965983e+00 -1.505306839942932129e+00
-3.921827023520433109e+00 -1.496874332427978516e+00
-3.913141095468253727e+00 -1.488440990447998047e+00
-3.904455218540149986e+00 -1.480007529258728027e+00
-3.895769306501919882e+00 -1.471575021743774414e+00
-3.887083468420036603e+00 -1.463142514228820801e+00
-3.878397584986599256e+00 -1.454709172248840332e+00
-3.869711659755526334e+00 -1.446276545524597168e+00
-3.861025762871284517e+00 -1.437844038009643555e+00
-3.852339890839859837e+00 -1.429411411285400391e+00
-3.843654018961608632e+00 -1.420978069305419922e+00
-3.834968104764350461e+00 -1.412545561790466309e+00
-3.826282218268962421e+00 -1.404113888740539551e+00
-3.817596324719622736e+00 -1.395681381225585938e+00
-3.808910458815883526e+00 -1.387248754501342773e+00
-3.800224559708468508e+00 -1.378816246986389160e+00
-3.791538638069713141e+00 -1.370384573936462402e+00
-3.782852770570959589e+00 -1.361952066421508789e+00
-3.774166906767970620e+00 -1.353520274162292480e+00
-3.765481030023900111e+00 -1.345087766647338867e+00
-3.756795119578456355e+00 -1.336655974388122559e+00
-3.748109223112261024e+00 -1.328224301338195801e+00
-3.739423347323524549e+00 -1.319792628288269043e+00
-3.730737429126206095e+00 -1.311360955238342285e+00
-3.722051577121266330e+00 -1.302929162979125977e+00
-3.713365664197652016e+00 -1.294497489929199219e+00
-3.704679735976083688e+00 -1.286066532135009766e+00
-3.695993869989676384e+00 -1.277634859085083008e+00
-3.687308019863064779e+00 -1.269203901290893555e+00
-3.678622088904873522e+00 -1.260773062705993652e+00
-3.669936232145071031e+00 -1.252342224121093750e+00
-3.661250311645260158e+00 -1.243911266326904297e+00
-3.652564437366765393e+00 -1.235480427742004395e+00
-3.643878554801473602e+00 -1.227049469947814941e+00
-3.635192653134445617e+00 -1.218619465827941895e+00
-3.626506762450233623e+00 -1.210189461708068848e+00
-3.617820872408112010e+00 -1.201759338378906250e+00
-3.609134963144495334e+00 -1.193329334259033203e+00
-3.600449133505907895e+00 -1.184899330139160156e+00
-3.591763195704384515e+00 -1.176470041275024414e+00
-3.583077285387287425e+00 -1.168040871620178223e+00
-3.574391452163673932e+00 -1.159611582756042480e+00
-3.565705529425397646e+00 -1.151182413101196289e+00
-3.557019612658295582e+00 -1.142753124237060547e+00
-3.548333767410239314e+00 -1.134324669837951660e+00
-3.539647858046817142e+00 -1.125896334648132324e+00
-3.530961997970627486e+00 -1.117468833923339844e+00
-3.522276064002788143e+00 -1.109040379524230957e+00
-3.513590215575287168e+00 -1.100612878799438477e+00
-3.504904302616541845e+00 -1.092185258865356445e+00
-3.496218451626031953e+00 -1.083758473396301270e+00
-3.487532535290027713e+00 -1.075331687927246094e+00
-3.478846655279983935e+00 -1.066905021667480469e+00
-3.470160748237835158e+00 -1.058478236198425293e+00
-3.461474822506118265e+00 -1.050052404403686523e+00
-3.452788988449653651e+00 -1.041626453399658203e+00
-3.444103098217174530e+00 -1.033201336860656738e+00
-3.435417220008483596e+00 -1.024776220321655273e+00
-3.426731314694355657e+00 -1.016352057456970215e+00
-3.418045446079814198e+00 -1.007927656173706055e+00
-3.409359512659658087e+00 -9.995034933090209961e-01
-3.400673614843955139e+00 -9.910800457000732422e-01
-3.391987724994787179e+00 -9.826574325561523438e-01
-3.383301853796073289e+00 -9.742348194122314453e-01
-3.374615987993563326e+00 -9.658131003379821777e-01
-3.365930094044440768e+00 -9.573913216590881348e-01
-3.357244179043766152e+00 -9.489703178405761719e-01
-3.348558288154213969e+00 -9.405502080917358398e-01
-3.339872419200406117e+00 -9.321301579475402832e-01
-3.331186555599311649e+00 -9.237108826637268066e-01
-3.322500642555013872e+00 -9.152923822402954102e-01
-3.313814748434434687e+00 -9.068747162818908691e-01
-3.305128875477012951e+00 -8.984571695327758789e-01
-3.296442942385930941e+00 -8.900402784347534180e-01
-3.287757039094269640e+00 -8.816243410110473633e-01
-3.279071171122592165e+00 -8.732084035873413086e-01
-3.270385316024439160e+00 -8.647940158843994141e-01
-3.261699427453387479e+00 -8.563797473907470703e-01
-3.253013529469882759e+00 -8.479670286178588867e-01
-3.244327622332729533e+00 -8.395543694496154785e-01
-3.235641729577599435e+00 -8.311433792114257812e-01
-3.226955854403765755e+00 -8.227324485778808594e-01
-3.218269941131704837e+00 -8.143230676651000977e-01
-3.209584087135528563e+00 -8.059145212173461914e-01
-3.200898208045630966e+00 -7.975068688392639160e-01
-3.192212253450247950e+00 -7.891008257865905762e-01
-3.183526398050005035e+00 -7.806956171989440918e-01
-3.174840491554045574e+00 -7.722920775413513184e-01
-3.166154610355592869e+00 -7.638893127441406250e-01
-3.157468746373989443e+00 -7.554882764816284180e-01
-3.148782852052625980e+00 -7.470880150794982910e-01
-3.140096985230698579e+00 -7.386894822120666504e-01
-3.131411026521371710e+00 -7.302925586700439453e-01
-3.122725167436577909e+00 -7.218964099884033203e-01
-3.114039289728531834e+00 -7.135028243064880371e-01
-3.105353415488861124e+00 -7.051100730895996094e-01
-3.096667537124901948e+00 -6.967197656631469727e-01
-3.087981652491603501e+00 -6.883302927017211914e-01
-3.079295735360625397e+00 -6.799433231353759766e-01
-3.070609887846959651e+00 -6.715579628944396973e-01
-3.061924008440656042e+00 -6.631743311882019043e-01
-3.053238013123760641e+00 -6.547923088073730469e-01
-3.044552143465693916e+00 -6.464127898216247559e-01
-3.035866277107784672e+00 -6.380349397659301758e-01
-3.027180367857409848e+00 -6.296595335006713867e-01
-3.018494492697283871e+00 -6.212866306304931641e-01
-3.009808608382922301e+00 -6.129162311553955078e-01
-3.001122716437681692e+00 -6.045482754707336426e-01
-2.992436835366602210e+00 -5.961828231811523438e-01
-2.983750927239147810e+00 -5.878215432167053223e-01
-2.975065071607993161e+00 -5.794619321823120117e-01
-2.966379221386281184e+00 -5.711064338684082031e-01
-2.957693308129347720e+00 -5.627533197402954102e-01
-2.949007425481820821e+00 -5.544044971466064453e-01
-2.940321462181671119e+00 -5.460588932037353516e-01
-2.931635555253712333e+00 -5.377166271209716797e-01
-2.922949686129372893e+00 -5.293793678283691406e-01
-2.914263779844503688e+00 -5.210446119308471680e-01
-2.905577915409446543e+00 -5.127148032188415527e-01
-2.896892033061762906e+00 -5.043891072273254395e-01
-2.888206144441518575e+00 -4.960683882236480713e-01
-2.879520288764902070e+00 -4.877509772777557373e-01
-2.870834418716912584e+00 -4.794393777847290039e-01
-2.862148520611490277e+00 -4.711319208145141602e-01
-2.853462648646287292e+00 -4.628294408321380615e-01
-2.844776778099358250e+00 -4.545319080352783203e-01
-2.836090883583508582e+00 -4.462393522262573242e-01
-2.827404906551029384e+00 -4.379526078701019287e-01
-2.818718993135480577e+00 -4.296716451644897461e-01
-2.810033116336304815e+00 -4.213964939117431641e-01
-2.801347253912741309e+00 -4.131279587745666504e-01
-2.792661357969872249e+00 -4.048660695552825928e-01
-2.783975451139036661e+00 -3.966116011142730713e-01
-2.775289590968113895e+00 -3.883637785911560059e-01
-2.766603720004675804e+00 -3.801242709159851074e-01
-2.757917852004532655e+00 -3.718929886817932129e-01
-2.749231981282639126e+00 -3.636700510978698730e-01
-2.740546085906816920e+00 -3.554561734199523926e-01
-2.731860185186624435e+00 -3.472506105899810791e-01
-2.723174336998412937e+00 -3.390549719333648682e-01
-2.714488347027445236e+00 -3.308692872524261475e-01
-2.705802436834944036e+00 -3.226935267448425293e-01
-2.697116575473119671e+00 -3.145277202129364014e-01
-2.688430702335061540e+00 -3.063726723194122314e-01
-2.679744804082326404e+00 -2.982292473316192627e-01
-2.671058887815255911e+00 -2.900974154472351074e-01
-2.662373073369971088e+00 -2.819771468639373779e-01
-2.653687173481048767e+00 -2.738684713840484619e-01
-2.645001260845450730e+00 -2.657730579376220703e-01
-2.636315381835180105e+00 -2.576901018619537354e-01
-2.627629517247564994e+00 -2.496203929185867310e-01
-2.618943631989034238e+00 -2.415639311075210571e-01
-2.610257760478297939e+00 -2.335215210914611816e-01
-2.601571799215770753e+00 -2.254940271377563477e-01
-2.592885878039596914e+00 -2.174823135137557983e-01
-2.584199989395424168e+00 -2.094879299402236938e-01
-2.575514116904918271e+00 -2.015110403299331665e-01
-2.566828237588024475e+00 -1.935522854328155518e-01
-2.558142360457055009e+00 -1.856126338243484497e-01
-2.549456488927343667e+00 -1.776936352252960205e-01
-2.540770587535358782e+00 -1.697962433099746704e-01
-2.532084724807635912e+00 -1.619203686714172363e-01
-2.523398828203228028e+00 -1.540668010711669922e-01
-2.514712963758877429e+00 -1.462373137474060059e-01
-2.506027064589428477e+00 -1.384326666593551636e-01
-2.497341072237177162e+00 -1.306536942720413208e-01
-2.488655186631728355e+00 -1.229011937975883484e-01
-2.479969322971838253e+00 -1.151752695441246033e-01
-2.471283439761888800e+00 -1.074774414300918579e-01
-2.462597536170697321e+00 -9.980947524309158325e-02
-2.453911649488540014e+00 -9.217052161693572998e-02
-2.445225796305531052e+00 -8.456301689147949219e-02
-2.436539892851666167e+00 -7.698698341846466064e-02
-2.427854037007447285e+00 -6.944326311349868774e-02
-2.419168146874381087e+00 -6.193266436457633972e-02
-2.410482291756029571e+00 -5.445686355233192444e-02
-2.401796372770685029e+00 -4.701585695147514343e-02
-2.393110540551141696e+00 -3.961131721735000610e-02
-2.384424535126452138e+00 -3.224569559097290039e-02
-2.375738616030684369e+00 -2.491901628673076630e-02
-2.367052759800302386e+00 -1.763373799622058868e-02
-2.358366872931836777e+00 -1.039237156510353088e-02
-2.349680981189080420e+00 -3.194868564605712891e-03
-2.340995130787686840e+00 3.955377731472253799e-03
-2.332309213724106378e+00 1.105759292840957642e-02
-2.323623367645748061e+00 1.811093278229236603e-02
-2.314937452116005545e+00 2.511287666857242584e-02
-2.306251568166621357e+00 3.206185996532440186e-02
-2.297565715254188401e+00 3.895697370171546936e-02
-2.288879841578990160e+00 4.579576477408409119e-02
-2.280193927585738134e+00 5.257660523056983948e-02
-2.271507946505198383e+00 5.929859355092048645e-02
-2.262822088711573532e+00 6.595762073993682861e-02
-2.254136197048670187e+00 7.255454361438751221e-02
-2.245450335640015727e+00 7.908517867326736450e-02
-2.236764421075417619e+00 8.554877340793609619e-02
-2.228078545825046941e+00 9.194266796112060547e-02
-2.219392660832416819e+00 9.826540201902389526e-02
-2.210706787601797174e+00 1.045152619481086731e-01
-2.202020916119292959e+00 1.106888949871063232e-01
-2.193335040775664879e+00 1.167846620082855225e-01
-2.184649130351850488e+00 1.228000745177268982e-01
-2.175963283529326553e+00 1.287343055009841919e-01
-2.167277390491366695e+00 1.345840692520141602e-01
-2.158591504148493545e+00 1.403476446866989136e-01
-2.149905625854288349e+00 1.460226178169250488e-01
-2.141219767617229763e+00 1.516064554452896118e-01
-2.132533842600974339e+00 1.570975482463836670e-01
-2.123847972051041921e+00 1.624925136566162109e-01
-2.115162123618197665e+00 1.677897721529006958e-01
-2.106476049890396496e+00 1.729875802993774414e-01
-2.097790147038471886e+00 1.780826598405838013e-01
-2.089104251254656930e+00 1.830734014511108398e-01
-2.080418375425595823e+00 1.879573017358779907e-01
-2.071732455035489640e+00 1.927318274974822998e-01
-2.063046590930888158e+00 1.973945498466491699e-01
-2.054360713641827818e+00 2.019437849521636963e-01
-2.045674870768575460e+00 2.063770741224288940e-01
-2.036988952725148572e+00 2.106918841600418091e-01
-2.028303097973127134e+00 2.148866057395935059e-01
-2.019617204739565519e+00 2.189578413963317871e-01
-2.010931287409201573e+00 2.229040265083312988e-01
-2.002245426083812951e+00 2.267235070466995239e-01
-1.993559562087256376e+00 2.304120510816574097e-01
-1.984873668964564741e+00 2.339697629213333130e-01
-1.976187789128496242e+00 2.373916208744049072e-01
-1.967501878344477095e+00 2.406775951385498047e-01
-1.958816036192365440e+00 2.438244223594665527e-01
-1.950130168790698448e+00 2.468296289443969727e-01
-1.941444256300051796e+00 2.496923506259918213e-01
-1.932758381922446755e+00 2.524092495441436768e-01
-1.924072519346392562e+00 2.549778819084167480e-01
-1.915386611162219310e+00 2.573974132537841797e-01
-1.906700736501320659e+00 2.596645355224609375e-01
-1.898014875193195561e+00 2.617751359939575195e-01
-1.889328981308828759e+00 2.637250125408172607e-01
-1.880642894927006870e+00 2.655116915702819824e-01
-1.871956987421844687e+00 2.671310305595397949e-01
-1.863271136564462305e+00 2.685789167881011963e-01
-1.854585238283246174e+00 2.698520123958587646e-01
-1.845899376844094109e+00 2.709511518478393555e-01
-1.837213502092107431e+00 2.718746960163116455e-01
-1.828527580019741805e+00 2.726234793663024902e-01
-1.819841726250061464e+00 2.731982767581939697e-01
-1.811155826099141164e+00 2.735974490642547607e-01
-1.802469994568540512e+00 2.738209962844848633e-01
-1.793784052220197989e+00 2.738648653030395508e-01
-1.785098196347216781e+00 2.737231552600860596e-01
-1.776412313075115268e+00 2.733884155750274658e-01
-1.767726458884000040e+00 2.728565335273742676e-01
-1.759040566823959928e+00 2.721208930015563965e-01
-1.750354641946203493e+00 2.711757123470306396e-01
-1.741668800382297100e+00 2.700126469135284424e-01
-1.732982909716716646e+00 2.686250507831573486e-01
-1.724297043221144854e+00 2.670055627822875977e-01
-1.715611125111091928e+00 2.651441693305969238e-01
-1.706925234703799088e+00 2.630351185798645020e-01
-1.698239390785301062e+00 2.606701254844665527e-01
-1.689553519039200369e+00 2.580433189868927002e-01
-1.680867617692947125e+00 2.551556527614593506e-01
-1.672181751945384764e+00 2.520070075988769531e-01
-1.663495675923640338e+00 2.485973984003067017e-01
-1.654809777957024330e+00 2.449277639389038086e-01
-1.646123909872960978e+00 2.409963458776473999e-01
-1.637438001588780168e+00 2.368073016405105591e-01
-1.628752124086759068e+00 2.323656380176544189e-01
-1.620066240951697933e+00 2.276795804500579834e-01
-1.611380385347776834e+00 2.227565795183181763e-01
-1.602694492568376150e+00 2.176033556461334229e-01
-1.594008601497067579e+00 2.122272849082946777e-01
-1.585322721388503719e+00 2.066341936588287354e-01
-1.576636835974350559e+00 2.008091360330581665e-01
-1.567950937189261928e+00 1.947298049926757812e-01
-1.559265084385837774e+00 1.883762925863265991e-01
-1.550579197830730838e+00 1.817270070314407349e-01
-1.541893327107657585e+00 1.747605502605438232e-01
-1.533207446650619366e+00 1.674593687057495117e-01
-1.524521545514696097e+00 1.598600149154663086e-01
-1.515835680411118602e+00 1.520403027534484863e-01
-1.507149788336508589e+00 1.440789401531219482e-01
-1.498463903450715895e+00 1.360537856817245483e-01
-1.489778024094568831e+00 1.280443817377090454e-01
-1.481092117526403129e+00 1.201277747750282288e-01
-1.472406244357701288e+00 1.123271286487579346e-01
-1.463720386045654465e+00 1.045869216322898865e-01
-1.455034499945996984e+00 9.684676676988601685e-02
-1.446348613523598337e+00 8.904612064361572266e-02
-1.437662508654072857e+00 8.112122118473052979e-02
-1.428976659461103083e+00 7.301326841115951538e-02
-1.420290760720851031e+00 6.468161195516586304e-02
-1.411604889734847212e+00 5.614535883069038391e-02
-1.402919020911396641e+00 4.743684455752372742e-02
-1.394233117181602255e+00 3.858749940991401672e-02
-1.385547250482869197e+00 2.962715737521648407e-02
-1.376861361250189431e+00 2.058811299502849579e-02
-1.368175461316678110e+00 1.150851417332887650e-02
-1.359489591377651907e+00 2.474418375641107559e-03
-1.350803710550227521e+00 -6.413020193576812744e-03
-1.342117812318127879e+00 -1.504947431385517120e-02
-1.333431957473148133e+00 -2.333307079970836639e-02
-1.324746063758182713e+00 -3.116105310618877411e-02
-1.316060189090259680e+00 -3.843820095062255859e-02
-1.307374322321914750e+00 -4.517356306314468384e-02
-1.298688423360473188e+00 -5.145916342735290527e-02
-1.290002553582901834e+00 -5.738442391157150269e-02
-1.281316650817528435e+00 -6.304215639829635620e-02
-1.272630785134080122e+00 -6.852426379919052124e-02
-1.263944879932707765e+00 -7.392184436321258545e-02
-1.255259018723212439e+00 -7.931780815124511719e-02
-1.246573116906716017e+00 -8.478253334760665894e-02
-1.237887247185847750e+00 -9.038634598255157471e-02
-1.229201378816720425e+00 -9.619814902544021606e-02
-1.220515496418541623e+00 -1.022865995764732361e-01
-1.211829389095954612e+00 -1.087229847908020020e-01
-1.203143523497155920e+00 -1.155594438314437866e-01
-1.194457611796427621e+00 -1.228000968694686890e-01
-1.185771752951713776e+00 -1.304425597190856934e-01
-1.177085861720257531e+00 -1.384826153516769409e-01
-1.168400021622637119e+00 -1.469169408082962036e-01
-1.159714095966454250e+00 -1.557464152574539185e-01
-1.151028208790643159e+00 -1.650497168302536011e-01
-1.142342361647159965e+00 -1.749734133481979370e-01
-1.133656490588393018e+00 -1.856625229120254517e-01
-1.124970603404404690e+00 -1.972644478082656860e-01
-1.116284689505959049e+00 -2.099167704582214355e-01
-1.107598805946843123e+00 -2.236102968454360962e-01
-1.098912950190215509e+00 -2.382200360298156738e-01
-1.090227067108913594e+00 -2.536191642284393311e-01
-1.081541172643484261e+00 -2.696800827980041504e-01
-1.072855310034610321e+00 -2.862637639045715332e-01
-1.064169435852718726e+00 -3.031903803348541260e-01
-1.055483540033254508e+00 -3.202734887599945068e-01
-1.046797644063215182e+00 -3.373259902000427246e-01
-1.038111763894425055e+00 -3.541589975357055664e-01
-1.029425911731048249e+00 -3.705828189849853516e-01
-1.020739995839564873e+00 -3.864051997661590576e-01
-1.012054131525570222e+00 -4.014323651790618896e-01
-1.003368231002438327e+00 -4.155020117759704590e-01
-9.946821522284455819e-01 -4.285403192043304443e-01
-9.859963012248768033e-01 -4.404934942722320557e-01
-9.773104127023426457e-01 -4.513134956359863281e-01
-9.686245494387427657e-01 -4.610524773597717285e-01
-9.599386295503481437e-01 -4.698687195777893066e-01
-9.512527600342358669e-01 -4.779211580753326416e-01
-9.425668795182289283e-01 -4.854310750961303711e-01
-9.338809981405238325e-01 -4.927554130554199219e-01
-9.251951375532303512e-01 -5.002744197845458984e-01
-9.165092509706674884e-01 -5.083583593368530273e-01
-9.078233358609623105e-01 -5.173518657684326172e-01
-8.991374823714243236e-01 -5.275936722755432129e-01
-8.904515637645005199e-01 -5.393630266189575195e-01
-8.817656778375342341e-01 -5.527724027633666992e-01
-8.730798124574407071e-01 -5.679039359092712402e-01
-8.643939284260089284e-01 -5.847302675247192383e-01
-8.557080563682236685e-01 -6.030625700950622559e-01
-8.470221547887063496e-01 -6.226763725280761719e-01
-8.383362968179316477e-01 -6.431127190589904785e-01
-8.296503980426550573e-01 -6.637892127037048340e-01
-8.209645331039009397e-01 -6.841062307357788086e-01
-8.122786275763584918e-01 -7.034325599670410156e-01
-8.035927619603087102e-01 -7.211900353431701660e-01
-7.949068754601738007e-01 -7.371267080307006836e-01
-7.862210183264345398e-01 -7.511342167854309082e-01
-7.775351485491822645e-01 -7.633326053619384766e-01
-7.688490281008053540e-01 -7.740324735641479492e-01
-7.601631751663275871e-01 -7.836977243423461914e-01
-7.514772578626658373e-01 -7.929811477661132812e-01
-7.427913946665252176e-01 -8.026008605957031250e-01
-7.341055159994032131e-01 -8.133587241172790527e-01
-7.254196244342873134e-01 -8.258950710296630859e-01
-7.167337554344906936e-01 -8.405851125717163086e-01
-7.080478762876644128e-01 -8.575158715248107910e-01
-6.993619911996875604e-01 -8.764337897300720215e-01
-6.906761073427274411e-01 -8.968237638473510742e-01
-6.819902047511335885e-01 -9.179343581199645996e-01
-6.733043623051708781e-01 -9.387475848197937012e-01
-6.646184802748164033e-01 -9.582850933074951172e-01
-6.559325627597188957e-01 -9.761162400245666504e-01
-6.472466803934194823e-01 -9.919196367263793945e-01
-6.385607961313211067e-01 -1.005661249160766602e+00
-6.298749425480695274e-01 -1.018097281455993652e+00
-6.211890540996163335e-01 -1.030124187469482422e+00
-6.125031636439244309e-01 -1.042600870132446289e+00
-6.038173163024376233e-01 -1.056298613548278809e+00
-5.951314165842153114e-01 -1.071971893310546875e+00
-5.864455431144686148e-01 -1.089881777763366699e+00
-5.777596393610755499e-01 -1.109299182891845703e+00
-5.690737679603549148e-01 -1.129378437995910645e+00
-5.603878652846858710e-01 -1.149304509162902832e+00
-5.517018011260974575e-01 -1.168316125869750977e+00
-5.430159291472674843e-01 -1.185669302940368652e+00
-5.343300220021273139e-01 -1.201263189315795898e+00
-5.256441537662452923e-01 -1.215934872627258301e+00
-5.169585020563290945e-01 -1.230588555335998535e+00
-5.082723793358518982e-01 -1.245923876762390137e+00
-4.995867317253799289e-01 -1.262379884719848633e+00
-4.909006545638227026e-01 -1.280357718467712402e+00
-4.822149519819215469e-01 -1.299580454826354980e+00
-4.735288918249241918e-01 -1.319055914878845215e+00
-4.648431869501309377e-01 -1.337785840034484863e+00
-4.561571183886922176e-01 -1.355458736419677734e+00
-4.474714319150950859e-01 -1.372387051582336426e+00
-4.387853177224788626e-01 -1.388912677764892578e+00
-4.300992458864488777e-01 -1.405475616455078125e+00
-4.214135803986128193e-01 -1.422587752342224121e+00
-4.127274844017292943e-01 -1.440712928771972656e+00
-4.040418282721578436e-01 -1.459611892700195312e+00
-3.953557442839072955e-01 -1.478582024574279785e+00
-3.866700756068330302e-01 -1.496969938278198242e+00
-3.779839666586953251e-01 -1.514761209487915039e+00
-3.692982706207104671e-01 -1.532302498817443848e+00
-3.606122078061714253e-01 -1.549919962882995605e+00
-3.519265522087779430e-01 -1.567711353302001953e+00
-3.432404295038166131e-01 -1.585670828819274902e+00
-3.345547502692063357e-01 -1.603784561157226562e+00
-3.258686940121170439e-01 -1.622044682502746582e+00
-3.171829949028228124e-01 -1.640438318252563477e+00
-3.084968955203842289e-01 -1.658957004547119141e+00
-2.998112357324092536e-01 -1.677589178085327148e+00
-2.911251613345057221e-01 -1.696324944496154785e+00
-2.824394891972903388e-01 -1.715152502059936523e+00
-2.737533861349122910e-01 -1.734063863754272461e+00
-2.650677234808396232e-01 -1.753046512603759766e+00
-2.563816429139535447e-01 -1.772090673446655273e+00
-2.476959766569552246e-01 -1.791185617446899414e+00
-2.390098532346092430e-01 -1.810321688652038574e+00
-2.303241637547374931e-01 -1.829487323760986328e+00
-2.216381148078668817e-01 -1.848673343658447266e+00
-2.129520137553757853e-01 -1.867871284484863281e+00
-2.042663355146025761e-01 -1.887081265449523926e+00
-1.955802847261854105e-01 -1.906307220458984375e+00
-1.868945880494207734e-01 -1.925549507141113281e+00
-1.782084995138485672e-01 -1.944812893867492676e+00
-1.695228132782916897e-01 -1.964097380638122559e+00
-1.608367162655343630e-01 -1.983407616615295410e+00
-1.521510322293604112e-01 -2.002743482589721680e+00
-1.434649665580840228e-01 -2.022109508514404297e+00
-1.347793009088293914e-01 -2.041506290435791016e+00
-1.260931961801279866e-01 -2.060937881469726562e+00
-1.174075398617945298e-01 -2.080404520034790039e+00
-1.087214214662880069e-01 -2.099910736083984375e+00
-1.000357630814676241e-01 -2.119456768035888672e+00
-9.134966069541652911e-02 -2.139047384262084961e+00
-8.266397588011786812e-02 -2.158682346343994141e+00
-7.397794303032081964e-02 -2.178366184234619141e+00
-6.529221664633462485e-02 -2.198097944259643555e+00
-5.660613993053786874e-02 -2.217878103256225586e+00
-4.792050382367946115e-02 -2.237704038619995117e+00
-3.923440420107948690e-02 -2.257576227188110352e+00
-3.054868508345384703e-02 -2.277491807937622070e+00
-2.186261258830971346e-02 -2.297451972961425781e+00
-1.317693769244786088e-02 -2.317452907562255859e+00
-4.490876337089103575e-03 -2.337496280670166016e+00
4.195253386500480408e-03 -2.357579708099365234e+00
1.288088987666799815e-02 -2.377700805664062500e+00
2.156700088870685053e-02 -2.397861003875732422e+00
3.025264939077326048e-02 -2.418056488037109375e+00
3.893875064526389207e-02 -2.438289165496826172e+00
4.762441152025540664e-02 -2.458554744720458984e+00
5.631051537109069832e-02 -2.478855133056640625e+00
6.499620512424000851e-02 -2.499186754226684570e+00
7.368224043129559253e-02 -2.519551038742065430e+00
8.236792731245561050e-02 -2.539944648742675781e+00
9.105402847448952619e-02 -2.560370683670043945e+00
9.973974006252958602e-02 -2.580826044082641602e+00
1.084257868388604495e-01 -2.601313352584838867e+00
1.171114656455329445e-01 -2.621830224990844727e+00
1.257975728062618315e-01 -2.642378568649291992e+00
1.344832562693170919e-01 -2.662956476211547852e+00
1.431693391758035727e-01 -2.683565855026245117e+00
1.518550173774160794e-01 -2.704204320907592773e+00
1.605410924961019059e-01 -2.724874258041381836e+00
1.692267641317125038e-01 -2.745573043823242188e+00
1.779128429837201486e-01 -2.766303062438964844e+00
1.865985273743302475e-01 -2.787062168121337891e+00
1.952846295069594063e-01 -2.807852029800415039e+00
2.039702777162885061e-01 -2.828671216964721680e+00
2.126563783834436727e-01 -2.849520444869995117e+00
2.213420210252148024e-01 -2.870398521423339844e+00
2.300281284660783965e-01 -2.891307115554809570e+00
2.387141999021882566e-01 -2.912245035171508789e+00
2.473999113618959578e-01 -2.933210611343383789e+00
2.560859887628060272e-01 -2.954205274581909180e+00
2.647716557449300012e-01 -2.975227594375610352e+00
2.734577571969878385e-01 -2.996278524398803711e+00
2.821434371623735005e-01 -3.017356395721435547e+00
2.908295092720811215e-01 -3.038462400436401367e+00
2.995152022524316116e-01 -3.059594631195068359e+00
3.082012914202362786e-01 -3.080754995346069336e+00
3.168869522887323154e-01 -3.101940155029296875e+00
3.255730459745904137e-01 -3.123152971267700195e+00
3.342587169935368197e-01 -3.144390344619750977e+00
3.429448021609445285e-01 -3.165654659271240234e+00
3.516304856584012151e-01 -3.186942815780639648e+00
3.603165745122932084e-01 -3.208257675170898438e+00
3.690022407767963308e-01 -3.229595661163330078e+00
3.776883467608408429e-01 -3.250959634780883789e+00
3.863740043506763699e-01 -3.272346973419189453e+00
3.950600790924266303e-01 -3.293759584426879883e+00
4.037457901585475017e-01 -3.315195322036743164e+00
4.124318730418749523e-01 -3.336655855178833008e+00
4.211175647845866177e-01 -3.358139038085937500e+00
4.298036347271259050e-01 -3.379647016525268555e+00
4.384892918524501693e-01 -3.401177167892456055e+00
4.471753671989990853e-01 -3.422731161117553711e+00
4.558614727932517874e-01 -3.444308757781982422e+00
4.645471481194610730e-01 -3.465908050537109375e+00
4.732332256436939666e-01 -3.487530469894409180e+00
4.819189041759582848e-01 -3.509174585342407227e+00
4.906050177939636492e-01 -3.530842304229736328e+00
4.992906616267977493e-01 -3.552530527114868164e+00
5.079767670998784901e-01 -3.574241876602172852e+00
5.166624246034179357e-01 -3.595973968505859375e+00
5.253485201751951772e-01 -3.617728710174560547e+00
5.340341690819686571e-01 -3.639503479003906250e+00
5.427202991069637328e-01 -3.661300897598266602e+00
5.514059535275526169e-01 -3.683118104934692383e+00
5.600920653199275012e-01 -3.704957246780395508e+00
5.687777230964998765e-01 -3.726816177368164062e+00
5.774638278465180630e-01 -3.748696804046630859e+00
5.861494518215523142e-01 -3.770596265792846680e+00
5.948355943179144401e-01 -3.792517423629760742e+00
6.035212781100782742e-01 -3.814457178115844727e+00
6.122073055662827779e-01 -3.836418151855468750e+00
6.208930360742207499e-01 -3.858397722244262695e+00
6.295790999118862086e-01 -3.880397796630859375e+00
6.382647729578403428e-01 -3.902416467666625977e+00
6.469508615968787568e-01 -3.924454689025878906e+00
6.556365323005303170e-01 -3.946511268615722656e+00
6.643226543946991747e-01 -3.968587875366210938e+00
6.730087314298176526e-01 -3.990683317184448242e+00
6.816944108492232202e-01 -4.012796401977539062e+00
6.903804419639441026e-01 -4.034928798675537109e+00
6.990661238304511915e-01 -4.057077884674072266e+00
7.077522452077964488e-01 -4.079246520996093750e+00
7.164379148270662023e-01 -4.101432800292968750e+00
7.251239990802521573e-01 -4.123637676239013672e+00
7.338096628105866825e-01 -4.145859241485595703e+00
7.424957927954936032e-01 -4.168099880218505859e+00
7.511814503983196278e-01 -4.190356254577636719e+00
7.598675394048506337e-01 -4.212631702423095703e+00
7.685532032022550641e-01 -4.234922885894775391e+00
7.772392800232890142e-01 -4.257232666015625000e+00
7.859249503313932017e-01 -4.279558181762695312e+00
7.946110533201700132e-01 -4.301901340484619141e+00
8.032967323949464777e-01 -4.324260234832763672e+00
8.119828232136918622e-01 -4.346636772155761719e+00
8.206684959763107523e-01 -4.369029045104980469e+00
8.293545753866979897e-01 -4.391438484191894531e+00
8.380402816739813687e-01 -4.413863182067871094e+00
8.467263322485351074e-01 -4.436305046081542969e+00
8.554119928791563687e-01 -4.458762168884277344e+00
8.640981057038400470e-01 -4.481235504150390625e+00
8.727837981625505837e-01 -4.503724098205566406e+00
8.814698858323849473e-01 -4.526229381561279297e+00
8.901555071339728453e-01 -4.548748970031738281e+00
8.988416308696665080e-01 -4.571285247802734375e+00
9.075277510446695395e-01 -4.593836784362792969e+00
9.162134091478749687e-01 -4.616402149200439453e+00
9.248994948338502553e-01 -4.638983726501464844e+00
9.335851207202202628e-01 -4.661579608917236328e+00
9.422712468656313511e-01 -4.684191226959228516e+00
9.509569295751451046e-01 -4.706816673278808594e+00
9.596430045448127721e-01 -4.729457378387451172e+00
9.683287053713744985e-01 -4.752111911773681641e+00
9.770147434053344515e-01 -4.774781703948974609e+00
9.857004236435150668e-01 -4.797464847564697266e+00
9.943865490058001466e-01 -4.820163726806640625e+00
1.003072230114558039e+00 -4.842875480651855469e+00
1.011758313611380578e+00 -4.865602493286132812e+00
1.020443972342219618e+00 -4.888341903686523438e+00
1.029130042377420562e+00 -4.911097049713134766e+00
1.037815709244417128e+00 -4.933864116668701172e+00
1.046501829792482852e+00 -4.956646442413330078e+00
1.055187485799181424e+00 -4.979441165924072266e+00
1.063873587339177140e+00 -5.002250671386718750e+00
1.072559259612110960e+00 -5.025072574615478516e+00
1.081245346847637290e+00 -5.047908782958984375e+00
1.089931045458941927e+00 -5.070756435394287109e+00
1.098617098961945260e+00 -5.093619346618652344e+00
1.107302767400820676e+00 -5.116493701934814453e+00
1.115988855620008824e+00 -5.139381885528564453e+00
1.124674950977802679e+00 -5.162283420562744141e+00
1.133360636235224428e+00 -5.185196399688720703e+00
1.142046714669423979e+00 -5.208123207092285156e+00
1.150732396526930268e+00 -5.231061458587646484e+00
1.159418465000188858e+00 -5.254013538360595703e+00
1.168104141074792324e+00 -5.276977062225341797e+00
1.176790266239130966e+00 -5.299953937530517578e+00
1.185475928195981243e+00 -5.322941780090332031e+00
1.194162020163351823e+00 -5.345942974090576172e+00
1.202847663327001326e+00 -5.368954658508300781e+00
1.211533762055852836e+00 -5.391980171203613281e+00
1.220219462015340595e+00 -5.415015697479248047e+00
1.228905546858021891e+00 -5.438064575195312500e+00
1.237591210414110021e+00 -5.461124420166015625e+00
1.246277287091709818e+00 -5.484196186065673828e+00
1.254963005753980010e+00 -5.507278919219970703e+00
1.263649078243616497e+00 -5.530374526977539062e+00
1.272334722447707511e+00 -5.553480148315429688e+00
1.281020798682833250e+00 -5.576598644256591797e+00
1.289706502940132671e+00 -5.599727153778076172e+00
1.298392568901131527e+00 -5.622868061065673828e+00
1.307078258362194045e+00 -5.646018981933593750e+00
1.315764345343309438e+00 -5.669182300567626953e+00
1.324450024673436310e+00 -5.692355632781982422e+00
1.333136102836428583e+00 -5.715540885925292969e+00
1.341822200899911222e+00 -5.738737583160400391e+00
1.350507865288792075e+00 -5.761943817138671875e+00
1.359193951896326302e+00 -5.785161972045898438e+00
1.367879656197688920e+00 -5.808389663696289062e+00
1.376565701082540061e+00 -5.831629276275634766e+00
1.385251424004338094e+00 -5.854878902435302734e+00
1.393937484964328233e+00 -5.878139972686767578e+00
1.402623180085014853e+00 -5.901410102844238281e+00
1.411309239514387581e+00 -5.924692630767822266e+00
1.419994915441684435e+00 -5.947983741760253906e+00
1.428680995157528333e+00 -5.971286773681640625e+00
1.437366715574801779e+00 -5.994598865509033203e+00
1.446052789304446584e+00 -6.017921924591064453e+00
1.454738440200429528e+00 -6.041254520416259766e+00
1.463424538789677376e+00 -6.064598083496093750e+00
1.472110228739432314e+00 -6.087950706481933594e+00
1.480796296472518092e+00 -6.111314296722412109e+00
1.489481977955309233e+00 -6.134686946868896484e+00
1.498168080349649323e+00 -6.158070564270019531e+00
1.506853708161008498e+00 -6.181462764739990234e+00
1.515539839350969809e+00 -6.204865932464599609e+00
1.524225525066536635e+00 -6.228277683258056641e+00
1.532911596327084514e+00 -6.251700401306152344e+00
1.541597229263971247e+00 -6.275131225585937500e+00
1.550283370742601141e+00 -6.298572540283203125e+00
1.558969043116118058e+00 -6.322022914886474609e+00
1.567655116334395249e+00 -6.345483779907226562e+00
1.576341183217232933e+00 -6.368953704833984375e+00
1.585026887280798435e+00 -6.392432212829589844e+00
1.593712973493785157e+00 -6.415921211242675781e+00
1.602398613416624595e+00 -6.439418792724609375e+00
1.611084720894563116e+00 -6.462926387786865234e+00
1.619770401642596225e+00 -6.486442565917968750e+00
1.628456479256070732e+00 -6.509968757629394531e+00
1.637142156394501447e+00 -6.533503532409667969e+00
1.645828278841839243e+00 -6.557048320770263672e+00
1.654513907816382856e+00 -6.580601215362548828e+00
1.663200017951624865e+00 -6.604164600372314453e+00
1.671885713028230525e+00 -6.627735614776611328e+00
1.680571759179416480e+00 -6.651317119598388672e+00
1.689257440723787029e+00 -6.674906253814697266e+00
1.697943558851664259e+00 -6.698505878448486328e+00
1.706629222750320585e+00 -6.722113132476806641e+00
1.715315299436098062e+00 -6.745730876922607422e+00
1.724000957632096709e+00 -6.769356250762939453e+00
1.732687050414690066e+00 -6.792991161346435547e+00
1.741372704754593492e+00 -6.816634178161621094e+00
1.750058816397330741e+00 -6.840287208557128906e+00
1.758744498608000528e+00 -6.863948345184326172e+00
1.767430593459505817e+00 -6.887619018554687500e+00
1.776116284788838096e+00 -6.911296844482421875e+00
1.784802330485672606e+00 -6.934985160827636719e+00
1.793488456363561356e+00 -6.958682060241699219e+00
1.802174133352250074e+00 -6.982386589050292969e+00
1.810860215794124040e+00 -7.006101131439208984e+00
1.819545893457968244e+00 -7.029822826385498047e+00
1.828232001066694812e+00 -7.053554534912109375e+00
1.836917649673889041e+00 -7.077293872833251953e+00
1.845603749582660491e+00 -7.101043224334716797e+00
1.854289404950727693e+00 -7.124800205230712891e+00
1.862975494661530007e+00 -7.148567199707031250e+00
1.871661159324801371e+00 -7.172341823577880859e+00
1.880347241963509441e+00 -7.196126461029052734e+00
1.889032955753610521e+00 -7.219919204711914062e+00
1.897719018034750293e+00 -7.243721961975097656e+00
1.906404708140265747e+00 -7.267532825469970703e+00
1.915090785586147870e+00 -7.291353702545166016e+00
1.923776462159045408e+00 -7.315182685852050781e+00
1.932462570182166273e+00 -7.339022159576416016e+00
1.941148216639278612e+00 -7.362869262695312500e+00
1.949834296647872778e+00 -7.386727333068847656e+00
1.958519964729958263e+00 -7.410593032836914062e+00
1.967206089774292899e+00 -7.434469223022460938e+00
1.975891759853673157e+00 -7.458353996276855469e+00
1.984577852689104027e+00 -7.482248306274414062e+00
1.993263529134031042e+00 -7.506151199340820312e+00
2.001949598033848421e+00 -7.530064105987548828e+00
2.010635703736094904e+00 -7.553986549377441406e+00
2.019321355997889089e+00 -7.577916622161865234e+00
2.028007465522790209e+00 -7.601857185363769531e+00
2.036693130448675948e+00 -7.625805377960205078e+00
2.045379213461333556e+00 -7.649763584136962891e+00
2.054064892641358053e+00 -7.673729896545410156e+00
2.062750949300368397e+00 -7.697706222534179688e+00
2.071436659726730412e+00 -7.721690654754638672e+00
2.080122722581565053e+00 -7.745684623718261719e+00
2.088808391919684926e+00 -7.769686698913574219e+00
2.097494528055039442e+00 -7.793698787689208984e+00
2.106180170731647650e+00 -7.817718505859375000e+00
2.114866300847850766e+00 -7.841749191284179688e+00
2.123551936105797733e+00 -7.865788936614990234e+00
2.132238010140539597e+00 -7.889840126037597656e+00
2.140923712211642904e+00 -7.913901329040527344e+00
2.149609777563103563e+00 -7.937975406646728516e+00
2.158295436508394172e+00 -7.962060451507568359e+00
2.166981536855828949e+00 -7.986159324645996094e+00
2.175667201459376532e+00 -8.010270118713378906e+00
2.184353332044185247e+00 -8.034396171569824219e+00
2.193038993649569779e+00 -8.058535575866699219e+00
2.201725048315615663e+00 -8.082690238952636719e+00
2.210410754543757239e+00 -8.106859207153320312e+00
2.219096842384700174e+00 -8.131045341491699219e+00
2.227782937580859102e+00 -8.155246734619140625e+00
2.236468589414552177e+00 -8.179465293884277344e+00
2.245154672678356000e+00 -8.203701019287109375e+00
2.253840375784205374e+00 -8.227952957153320312e+00
2.262526440500525649e+00 -8.252221107482910156e+00
2.271212135388195996e+00 -8.276503562927246094e+00
2.279898215134149364e+00 -8.300800323486328125e+00
2.288583876659929572e+00 -8.325107574462890625e+00
2.297269983936764071e+00 -8.349428176879882812e+00
2.305955628698024285e+00 -8.373758316040039062e+00
2.314641737172617120e+00 -8.398097991943359375e+00
2.323327396848104520e+00 -8.422445297241210938e+00
2.332013489085145164e+00 -8.446801185607910156e+00
2.340699156912034784e+00 -8.471161842346191406e+00
2.349385262738707070e+00 -8.495528221130371094e+00
2.358070965877896441e+00 -8.519898414611816406e+00
2.366757047826607341e+00 -8.544272422790527344e+00
2.375442682780369186e+00 -8.568647384643554688e+00
""")

k, p = 10**numpy.loadtxt(_psdata_wmap9, unpack=True)
WMAP9 = PowerSpectrum(k, p, sigma8=0.820)