from flet import *
import requests
import time

def main(page:Page):
    page.theme_mode=ThemeMode.LIGHT
    hf=HapticFeedback()
    sb=SnackBar(content=Text(weight=FontWeight.W_700,color='green',size=18))
    ad=AlertDialog(content=Text())
    bs=BottomSheet(content=Text())
    page.overlay.extend([hf,ad,sb,bs])
    textfield_column=Ref[Column]()
    add_page_column=Ref[Column]()
    data_tabel=Ref[DataTable]()
    checkbox=Ref[Checkbox]()
    download_btn=Ref[FloatingActionButton]()
    class HomeHeader(SafeArea):
        def __init__(self):
            super().__init__(content=None)
            self.content=Container(
                        height=100,
                        bgcolor=colors.WHITE60,
                        shadow=BoxShadow(0,10,'grey',blur_style=ShadowBlurStyle.OUTER),
                        content=Container(height=100,content=Text(col=11,spans=[TextSpan('Latha Mathavan Engineering College',TextStyle(25,weight=FontWeight.W_800,foreground=Paint(gradient=PaintLinearGradient((200,100),(10,130),colors=[colors.PINK,colors.BLUE_ACCENT]))))],text_align=TextAlign.CENTER),blur=Blur(1,1),alignment=Alignment(0,0)),
                        border_radius=BorderRadius(20,20,20,20),
                        width=page.width,
                        alignment=Alignment(0,0),
                        image_src='icon.png'       
            )
            self.col=11
            

    class SSHeader(HomeHeader):
        def __init__(self):
            HomeHeader.__init__(self)
            self.content.content=Container(height=100,content=ResponsiveRow(controls=[IconButton(icon=icons.ARROW_BACK_IOS_NEW,col=1,icon_color='Black',on_click=views_remove),Text(col=11,spans=[TextSpan('Latha Mathavan Engineering College',TextStyle(25,weight=FontWeight.W_800,foreground=Paint(gradient=PaintLinearGradient((200,100),(10,130),colors=[colors.PINK,colors.BLUE_ACCENT]))))],text_align=TextAlign.CENTER)],vertical_alignment=CrossAxisAlignment.CENTER),blur=Blur(1,1),alignment=Alignment(0,0))
           
    class HomeButton(Container):
        def  __init__(self,content=None,key=None,click=None,data=None):
            super().__init__()
            self.gradient=LinearGradient(colors=['pink','cyan'])
            self.content=content
            self.border_radius=20
            self.border=border.all(1,'white')
            self.shadow=BoxShadow(0,10,color='black',blur_style=ShadowBlurStyle.OUTER)
            self.alignment=Alignment(0,0)
            self.width=400
            self.height=60
            self.margin=margin.all(30)
            self.on_click=click
            self.key=key
            self.data=data
            self.col=6

    class InformationContainer(Container):
        def __init__(self,bgcolor='green',icon=icons.VERIFIED_USER_OUTLINED,msg=None):
            super().__init__()
            self.content=Row(controls=[Icon(icon,color='white'),Text(msg,size=15,color='white',weight=FontWeight.W_700,text_align=TextAlign.CENTER)],alignment=MainAxisAlignment.CENTER)
            self.shadow=BoxShadow(0,5,'grey',blur_style=ShadowBlurStyle.OUTER)
            self.padding=padding.all(10)
            self.bgcolor=bgcolor
            self.width=300
            self.border_radius=10

    class TextFields(TextField):
        def __init__(self,label=None,hinttext=None,colour='white',autofocus=False,ispassword=False):
            super().__init__()
            self.width=200
            self.border=InputBorder.UNDERLINE
            self.label=label
            self.hint_text=hinttext
            self.label_style=TextStyle(weight=FontWeight.W_700,size=13,color=colour)
            self.hint_style=TextStyle(weight=FontWeight.W_600,size=13,color=colour)
            self.text_style=TextStyle(weight=FontWeight.W_700,size=15,color=colour)
            self.border_color=colour
            self.border_width=2
            self.text_align=TextAlign.CENTER
            self.cursor_color=colour
            self.autofocus=autofocus
            self.password=ispassword
            self.can_reveal_password=ispassword

    register_number=TextFields('Student Register Number',None,autofocus=True)
    student_name=TextFields('Student Name',None)
    student_attendence=TextFields('Student Attendence','In Percentage')
    student_fees=TextFields('Student Fee Balance','In Ruppess')
    password=TextFields('Enter The Passsword',None,'black',ispassword=True)

    def download(e):
        hf.heavy_impact()
        hf.update()
        download_btn.current.content=ProgressRing(color='white')
        file_picker.get_directory_path()
        page.update()

    def add_controls_to_add_page(data):
        if data=='addstudent':
                    
            textfield_column.current.controls.extend([
                                        register_number,
                                        Divider(opacity=0),
                                        student_name,
                                        Divider(opacity=0),
                                        student_attendence,
                                        Divider(opacity=0),
                                        student_fees,
                                        Divider(opacity=0),
                                        ElevatedButton('Add',on_click=add_update_delete,key='add'),
                                        
                                    ]
            )
        
        elif data=='updatestudent':
            textfield_column.current.controls.extend([
                                        register_number,
                                        Divider(opacity=0),
                                        student_attendence,
                                        Divider(opacity=0),
                                        student_fees,
                                        Divider(opacity=0),
                                        ElevatedButton('Update',on_click=add_update_delete,key='update')
                                        
                                    ]
            )

        elif data=='deletestudent':
            textfield_column.current.controls.extend([
                                        register_number,
                                        Divider(opacity=0),
                                        ElevatedButton('Delete',on_click=add_update_delete,key='delete')

                                    ]
            )

        elif data=='downloadstudent':
            page.views.append(show_student_data())
            page.update()
            page.views[-1].controls.insert(1,ProgressBar(color='black',bgcolor='white',height=8,border_radius=50))
            page.update()
            response=request_manager(requests.get,'/Get-Student',None)
            page.views[-1].controls.pop(1)
            for i in response.json()['detail']:
                data_tabel.current.rows.append(
                    DataRow(
                        cells=[
                            DataCell(
                                Text(i['register_number'],weight=FontWeight.W_700,size=15)
                            ),
                            DataCell(
                                Text(i['student_name'],weight=FontWeight.W_700,size=15)
                            ),
                            DataCell(
                                Text(i['student_attedence'],weight=FontWeight.W_700,size=15)
                            ),
                            DataCell(
                                Text(i['student_fee'],weight=FontWeight.W_700,size=15)
                            )
                        ]
                    )
                )
        page.update()

    def check(e):
        hf.heavy_impact()
        password.error_text=None
        page.update(hf)
        print(e.control.data)
        if checkbox.current and checkbox.current.value:
            if e.control.data!='downloadstudent':
                page.views.append(add())
            add_controls_to_add_page(e.control.data)
        else:
            bs.open=True
            bs.content=Column(
                width=400,
                height=200,
                controls=[
                    password,
                    Row([Checkbox(ref=checkbox,label='Save Password Until Close The Session',label_style=TextStyle(weight=FontWeight.W_600,size=13,color='black'),check_color='white',active_color='green')],alignment=MainAxisAlignment.CENTER),
                    OutlinedButton('verify',on_click=views_add,key='staff_buttons',data=e.control.data)
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER
            )
        
        page.update()

    def request_manager(method,route,data):
        try:
            return method('https://bright-dawna-sivarajan-c060034e.koyeb.app'+route,json=data)
        except:
            sb.content.value='Please Turn On Your Network'
            sb.open=True
            page.update()

    def save_file(e:FilePickerResultEvent):
        if e.path:
            download_path=f'{e.path}/Latha Mathavan student Details.xlsx'
            response=request_manager(requests.get,'/Download-Student',None)
            try:
                with open(download_path,'wb') as f:
                    f.write(response.content)
                ad.content=ResponsiveRow([Text('Successfully Downloaded !',weight=FontWeight.W_700,size=18,color='green',text_align='center'),Text(f'Latha Mathavan Student Details.xlsx\n In {e.path}',weight=FontWeight.W_700,size=18,color=colors.BLUE_ACCENT,text_align='center')])
                ad.title=Image("1103-confetti.gif",width=50,height=50)
            except:
                ad.content=ResponsiveRow([Text('Failed To Download !',weight=FontWeight.W_700,size=18,color='red',text_align='center'),Text('Try To Choose Different Folder',weight=FontWeight.W_700,size=18,color=colors.BLUE_ACCENT,text_align='center')])
                ad.title=Image('comp_3.webp',width=75,height=75)
        else:
            ad.content=Text('Please Select a Folder To Download',weight=FontWeight.W_700,size=18,color='red',text_align='center')
            ad.title=Image('120-folder.gif',width=50,height=50)
        ad.open=True
        download_btn.current.content=Icon(icons.DOWNLOAD,color='white')
        page.update()

    file_picker=FilePicker(on_result=save_file)
    page.overlay.append(file_picker)


    def add_update_delete(e):
        data={'bool':0,'detail':"Input Field Couldn't Be Empty"}
        if e.control.key=='add':
            if register_number.value!="" and student_name.value!="" and student_attendence.value!="" and student_fees.value!="":
                e.control.text='Adding...'
                e.control.disable=True
                e.control.update()
                response=request_manager(requests.post,'/Add-Student',{'student_register_number':register_number.value.strip(),'student_name':student_name.value.title().strip(),'student_attedence':f'{student_attendence.value.strip()} %','student_fee':f'{student_fees.value.strip()} Rs'})
                e.control.text='Add'
                e.control.disable=False
                data=response.json()

        elif e.control.key=='update':
            if register_number.value!="" and student_attendence.value!="" and student_fees.value!="":
                e.control.text='Updating...'
                e.control.disable=True
                e.control.update()
                response=request_manager(requests.put,'/Update-Student',{'student_register_number':register_number.value.strip(),'student_name':student_name.value.title().strip(),'student_attedence':f'{student_attendence.value.strip()} %','student_fee':f'{student_fees.value.strip()} Rs'})
                e.control.text='Update'
                e.control.disable=False
                data=response.json()

        elif e.control.key=='delete':
            if register_number.value!="":
                e.control.text='Deleting...'
                e.control.disable=True
                e.control.update()
                response=request_manager(requests.delete,'/Delete-Student',{'student_register_number':register_number.value.strip(),'student_name':student_name.value.title().strip(),'student_attedence':f'{student_attendence.value.strip()} %','student_fee':f'{student_fees.value.strip()} Rs'})
                e.control.text='Delete'
                e.control.disable=False
                data=response.json()
        
        if data['bool']:
            add_page_column.current.controls.insert(0,InformationContainer(msg=data['detail']))
        else:
            add_page_column.current.controls.insert(0,InformationContainer(bgcolor='red',icon=icons.REPORT,msg=data['detail']))
        register_number.value=None
        student_fees.value=None
        student_attendence.value=None
        student_name.value=None
        page.update()
        time.sleep(2)
        add_page_column.current.controls.pop(0)
        page.update()
        
    def views_add(e):
        hf.heavy_impact()
        register_number.value=''
        student_attendence.value=''
        student_name.value=''
        student_fees.value=''
        page.update()
        if e.control.key=='student':
            page.views.append(student_page())

        elif e.control.key=='staff':
            page.views.append(staff_page())

        elif e.control.key=='staff_buttons':
          
            if password.value=='1234':
                if checkbox.current.value==False:
                    password.value=''
                password.error_text=None
                student_name.label='Student Name'
                if e.control.data!='downloadstudent':
                    page.views.append(add())
                add_controls_to_add_page(e.control.data)

                
            else:
                password.error_text='Incorrect Password'
                password.value=''
        page.update()
    
    

    def views_remove(e):
        hf.heavy_impact()
        page.update()
        page.views.pop()
        page.update()

    def show_student_page_details(e):
        hf.heavy_impact()
        page.update(hf)
        ad.content=Text("Input Field Couldn't Be Empty",weight=FontWeight.W_700,size=18,color='red')
        ad.title=Image('245-edit-document.gif',width=75,height=75)
        if register_number.value!="":
            e.control.text='Sumbiting...'
            e.control.disable=True
            e.control.update()
            response=request_manager(requests.get,'/Get-Single-Student',{'student_register_number':register_number.value,'student_name':None,'student_attedence':None,'student_fee':None})
            
            if isinstance(response.json()['detail'],dict):
                ad.content=Column(
                    width=300,
                    height=200,
                    controls=[
                        Container(
                            content=Column(
                                controls=[
                                    Text('Attedence',size=20,weight=FontWeight.W_800,color=colors.INDIGO_ACCENT),
                                    Text(response.json()['detail']['student_attedence'],size=20,weight=FontWeight.W_800,color=colors.DEEP_PURPLE_ACCENT),
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER
                            ),
                            padding=padding.all(10),
                            alignment=Alignment(0,0),
                            shadow=BoxShadow(0,5,'grey',blur_style=ShadowBlurStyle.OUTER),
                            border_radius=30
                        ),
                        Container(
                            content=Column(
                                controls=[
                                    Text('Fees Balance',size=20,weight=FontWeight.W_800,color=colors.INDIGO_ACCENT),
                                    Text(response.json()['detail']['student_fee'],size=20,weight=FontWeight.W_800,color=colors.DEEP_PURPLE_ACCENT)
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER
                                
                            ),
                            padding=padding.all(10),
                            alignment=Alignment(0,0),
                            shadow=BoxShadow(0,5,'grey',blur_style=ShadowBlurStyle.OUTER),
                            border_radius=30
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER
                )
                ad.title=ResponsiveRow([Image(src='giphy.webp',width=75,height=75,border_radius=50),Text(spans=[TextSpan(f"Hi,{response.json()['detail']['student_name']}".title(),TextStyle(22,weight=FontWeight.W_800,foreground=Paint(gradient=PaintLinearGradient((200,100),(10,130),colors=[colors.PINK,colors.BLUE_ACCENT]))))],text_align=TextAlign.CENTER)],alignment=MainAxisAlignment.CENTER)
                ad.alignment=Alignment(0,0)
                page.update()
            else:
                ad.content=Text(response.json()['detail'],weight=FontWeight.W_700,color='red',size=18,text_align='center')
                ad.title=Image('not_found.gif',width=75,height=75)
    
        ad.open=True
        e.control.text='Sumbit'
        e.control.disable=False
        page.update()


    def home_page():
        return View(
            controls=[
                HomeHeader(),
                Container(
                    content=Column(
                        expand=True,
                        controls=[
                            Stack(
                                controls=[
                                    Container(
                                        content=Column(
                                            controls=[
                                                Divider(opacity=0),
                                                HomeButton(content=Text(value='Student Login',text_align=TextAlign.CENTER,size=18,color='white',weight=FontWeight.W_700),key='student',click=views_add),
                                                HomeButton(content=Text(value='Staff Login',text_align=TextAlign.CENTER,size=18,color='white',weight=FontWeight.W_700),key='staff',click=views_add),
                                            ],
                                            width=page.width,
                                            horizontal_alignment=CrossAxisAlignment.CENTER
                                        ),
                                        width=500,
                                        height=300,
                                        shadow=BoxShadow(0,5,'grey',blur_style=ShadowBlurStyle.OUTER),
                                        border_radius=50,
                                        margin=margin.all(10),
                                        bgcolor=colors.WHITE70,
                                        border=border.all(1,'cyan')
                                    ),
                                    
                                ],
                               
                            )
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        alignment=MainAxisAlignment.CENTER
                    ),
                    expand=True,
                    width=page.width,
                    border_radius=20
                ),
                   
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER
        )
    
    def student_page():
        register_number.label='Your Register Number'
        return View(
            controls=[
                SSHeader(),
                
                Column(
                    controls=[
                        Divider(opacity=0,height=60),
                        Container(
                            content=Column(
                                controls=[

                                    Container(
                                        content=Column(
                                            controls=[
                                                register_number,
                                                Divider(opacity=0),
                                                
                                                
                                                ElevatedButton('sumbit',on_click=show_student_page_details)
                                                
                                            ],
                                            alignment=MainAxisAlignment.CENTER,
                                            horizontal_alignment=CrossAxisAlignment.CENTER
                                        ),
                                        height=200,
                                        width=300,
                            
                                        alignment=Alignment(0,0),
                                        border_radius=20,
                                        gradient=LinearGradient(['cyan','purple']),
                                        shadow=BoxShadow(0,20,'grey',blur_style=ShadowBlurStyle.OUTER),
                                    ),
                                        
                                ],
                
                                
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                            
                                
                            ),
                            alignment=Alignment(0,0),
                            
                            width=page.width,
                            
                        )
                    ],
                    scroll=ScrollMode.AUTO,
                    height=page.height-100,
                    alignment=MainAxisAlignment.CENTER
                )
            ],
           
        )

    def staff_page():

        return View(
            
            controls=[
                SSHeader(),
                Column(
                    controls=[
                        Container(
                            content=Column(
                                controls=[
                                    HomeButton(content=ResponsiveRow(controls=[Icon(icons.NOTE_ADD,color='white',col=2),Text(col=10,value='Add Stduent Details',text_align=TextAlign.CENTER,size=18,color='white',weight=FontWeight.W_700)],alignment=MainAxisAlignment.CENTER),data='addstudent',key='staff_buttons',click=check),
                                    HomeButton(content=ResponsiveRow(controls=[Icon(icons.EDIT_DOCUMENT,color='white',col=2),Text(col=10,value='Update Stduent Details',text_align=TextAlign.CENTER,size=18,color='white',weight=FontWeight.W_700)],alignment=MainAxisAlignment.CENTER),data='updatestudent',key='staff_buttons',click=check),
                                    HomeButton(content=ResponsiveRow(controls=[Icon(icons.DELETE,color='white',col=2),Text(col=10,value='Delete Stduent Details',text_align=TextAlign.CENTER,size=18,color='white',weight=FontWeight.W_700)],alignment=MainAxisAlignment.CENTER),data='deletestudent',key='staff_buttons',click=check),
                                    HomeButton(content=ResponsiveRow(controls=[Icon(icons.DOWNLOAD,color='white',col=2),Text(col=10,value='View and Download Stduent Details',text_align=TextAlign.CENTER,size=18,color='white',weight=FontWeight.W_700)],alignment=MainAxisAlignment.CENTER),data='downloadstudent',key='staff_buttons',click=check),
                                ],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                alignment=MainAxisAlignment.CENTER
                            ),
                            alignment=Alignment(0,0),
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    scroll=ScrollMode.AUTO,
                    height=page.height-100
                )
            ],
            
        )

    def add():
        register_number.label='Student Register Number'
        return View(
            
            controls=[
                SSHeader(),
                Column(
                    ref=add_page_column,
                    controls=[                
                        Container(
                            content=Column(
                                controls=[
                                    Container(
                                        content=Column(
                                            ref=textfield_column,
                                            alignment=MainAxisAlignment.CENTER,
                                            horizontal_alignment=CrossAxisAlignment.CENTER
                                        ),
                                        
                                        width=300,
                                        padding=padding.all(50),
                                        margin=margin.all(20),
                                        alignment=Alignment(0,0),
                                        border_radius=20,
                                        gradient=LinearGradient(['cyan','purple']),
                                        shadow=BoxShadow(0,20,'grey',blur_style=ShadowBlurStyle.OUTER),
                                    ),
                                        
                                ],
                
                                
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                            ),
                            alignment=Alignment(0,0),
                            width=page.width,
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    scroll=ScrollMode.AUTO,
                    height=page.height-100
                )
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            
        )
    def show_student_data():
        return View(
            controls=[
                SSHeader(),
                FloatingActionButton(ref=download_btn,content=Icon(icons.DOWNLOAD,color='white'),enable_feedback=True,bgcolor='black',on_click=download),
                Column(
                    controls=[
                        Row(
                            controls=[
                                DataTable(
                                    ref=data_tabel,
                                    
                                    columns=[
                                        DataColumn(
                                            Text('Register Number',weight=FontWeight.W_700,size=18)
                                        ),
                                        DataColumn(
                                            Text('Student Name',weight=FontWeight.W_700,size=18)
                                        ),
                                        DataColumn(
                                            Text('Attedence',weight=FontWeight.W_700,size=18)
                                        ),
                                        DataColumn(
                                            Text('Fee Balance',weight=FontWeight.W_700,size=18)
                                        )
                                    ],
                                    vertical_lines=BorderSide(1,'black'),
                                    show_bottom_border=True,
                                    expand=True,
                                    sort_ascending=True
                                    
                                )
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            scroll=ScrollMode.ADAPTIVE
                        )
                    ],
                    expand=True,
                    width=page.width,
                    scroll=ScrollMode.ADAPTIVE,
                    
                    horizontal_alignment=CrossAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER
        )
    page.views.clear()         
    page.views.append(home_page())

    page.on_view_pop=views_remove
    page.update()

app(main)