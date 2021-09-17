import random


class GetJs():
    def __init__(self, data, dtype='discrete'):
        self.data = data
        self.dtype = dtype

    def generate(self, element_id, method='morris_bar'):
        if method in ['morris_bar', 'morris_line', 'morris_area']:
            if method == 'morris_bar':
                Mtype = 'Bar'
            elif method == 'morris_line':
                Mtype = 'Line'
            else:
                Mtype = 'Area'
            if self.dtype == 'discrete':
                labels = list(self.data.keys())
                string_data = ""
                vals = list(self.data.values())
                for i in range(len(vals)):
                    string_data += '{ x: %d, y: ' % i+str(vals[i]) + ' },'
            else:
                sparse = len(self.data['counter'])
                min_val = self.data['min']
                max_val = self.data['max']
                range_val = max_val - min_val
                labels = []
                for i in range(sparse):
                    labels.append(str(min_val+i*range_val/sparse) +
                                  '~' + str(min_val+(i+1)*range_val/sparse))
                string_data = ""
                vals = self.data['counter']
                for i in range(len(vals)):
                    string_data += '{ x: %d, y: ' % i+str(vals[i]) + ' },'
            code = "xaxislabels = %s;\
        new Morris.%s({\
            element: %s,\
            behaveLikeLine: true,\
            data: [%s\
            ],\
            xkey: 'x',\
            ykeys: ['y'],\
            parseTime: false,\
            xLabelFormat: function (x) {\
                var index = parseInt(x.src.x);\
                return xaxislabels[index];\
            },\
            labels: ['Number'],\
            %sColors: ['#5969ff', '#ff407b'],\
            resize: true,\
        hideHover: 'auto',\
            gridTextSize: '14px'\
        });" % (str(labels), Mtype, element_id, string_data, Mtype.lower())
            return code, False
        elif method == 'morris_donut':
            if self.dtype == 'discrete':
                labels = list(self.data.keys())
                string_data = ""
                vals = list(self.data.values())
                for i in range(len(vals)):
                    string_data += ' { value: ' + \
                        str(vals[i])+', label: "%s" },' % labels[i]
            else:
                sparse = len(self.data['counter'])
                min_val = self.data['min']
                max_val = self.data['max']
                range_val = max_val - min_val
                labels = []
                for i in range(sparse):
                    labels.append(str(min_val+i*range_val/sparse) +
                                  '~' + str(min_val+(i+1)*range_val/sparse))
                string_data = ""
                vals = self.data['counter']
                for i in range(len(vals)):
                    string_data += ' { value: ' + \
                        str(vals[i])+', label: "%s" },' % labels[i]
            code = "new Morris.Donut({\
                element: '%s',\
                data: [\
                    %s\
                ],\
                labelColor: '#2e2f39',\
                   gridTextSize: '14px',\
                colors: [\
                        '#5969ff',\
                        '#ff407b',\
                        '#25d5f2',\
                        '#ffc750'\
                ],\
                formatter: function(x) { return x },\
        hideHover: 'auto',\
                  resize: true\
            });" % (element_id, string_data)
            return code, True
        else:
            raise ValueError('Unknown method!')

    def generate_random(self, element_id):
        if self.dtype == 'continuous':
            methods = ['morris_bar', 'morris_line',
                       'morris_area', 'morris_donut']
            return self.generate(
                element_id, methods[random.randint(0, len(methods)-1)])
        else:
            methods = ['morris_bar', 'morris_donut']
            return self.generate(
                element_id, methods[random.randint(0, len(methods)-1)])
