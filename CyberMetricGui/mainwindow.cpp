#include <cstdio>
#include <iostream>
#include <unistd.h>

#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "QImage"
#include "QSize"
#include "QLabel"
#include "QAction"
#include "QFileDialog"
#include "QFileInfo"

using namespace std;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    connect(ui->actionOpen_o, SIGNAL(triggered()), this, SLOT(open_file()));//连接控件和函数
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_clicked() //生成攻击图
{

    QLabel *imageLabel = new QLabel(this);//生成一个Qlabel对象
    string env = "cd " + outDir.toStdString() + "\n source /etc/profile \n source ~/.bash_profile \n ";
    string mulutilpath = "$MULVALROOT/utils/";
    string cmd = "graph_gen.sh h2v1s5.P -v -p";
    string holeCmd = env + mulutilpath + cmd;
    system(holeCmd.c_str());   //命令行调用
    QPixmap img1;
    img1.load(outDir + "/AttackGraph.png");
    img1 = scaleScroll(img1);  //调整图像，自适应scroll
    imageLabel->setPixmap(img1);//装载图片
    imageLabel->resize(img1.width(), img1.height());//调整label的大小
    //cout << img1.width() <<endl<< img1.height() << endl;
    ui->scrollArea->setWidgetResizable(1);
    ui->scrollArea->setWidget(imageLabel);
}

void MainWindow::open_file() //打开文件，获得文件名，绝对路径，把输入文件的名字修改
{
    inputPath = QFileDialog::getOpenFileName(this,    //包含文件名和绝对路径
        tr("Open Input File"), "/Users/Saint/Code/Cybermetric/mulval/testcases",
        tr("Prolog files (*.P)"));
    //cout << inputPath.toStdString().c_str() << endl;
    QFileInfo fi = QFileInfo(inputPath);
    outDir = fi.absolutePath();    //获得绝对路径
    cout << inputPath.toStdString().c_str() << endl;
    cout << outDir.toStdString().c_str() << endl;
    string renameFile = "cd " + outDir.toStdString() + "\n mv " + inputPath.toStdString() + " ./h2v1s5.P";
    system(renameFile.c_str());
}

void MainWindow::on_pushButton_2_clicked() //生成物理拓扑图
{
    QLabel *imageLabel = new QLabel(this);
    string env = "cd " + outDir.toStdString() + "\n source /etc/profile \n source ~/.bash_profile \n ";
    string mulutilpath = "$MULVALROOT/utils/";
    string cmd = "python " + mulutilpath + "topograph.py -d";
    string holeCmd = env + cmd;
    system(holeCmd.c_str());
    QPixmap img1;
    img1.load(outDir + "/originnet.png");
    img1 = scaleScroll(img1);
    imageLabel->setPixmap(img1);
    imageLabel->resize(img1.width(), img1.height());
    //cout << img1.width() <<endl<< img1.height() << endl;
    ui->scrollArea->setWidgetResizable(1);
    ui->scrollArea->setWidget(imageLabel);
}

void MainWindow::on_pushButton_3_clicked() //生成攻击路径示意图
{
    QLabel *imageLabel = new QLabel(this);
    string env = "cd " + outDir.toStdString() + "\n source /etc/profile \n source ~/.bash_profile \n ";//source导入环境变量
    string mulutilpath = "$MULVALROOT/utils/";//mul的环境变量
    string cmd = "python " + mulutilpath + "topograph.py -r";
    string holeCmd = env + cmd;
    system(holeCmd.c_str());
    QPixmap img1;
    img1.load(outDir + "/TopoAttackGraph.png");
    //cout << (double)img1.width() / (double)ui->scrollArea->width() << "\d" << (double)img1.height() / (double)ui->scrollArea->height() << endl;
    img1 = scaleScroll(img1);
    imageLabel->setPixmap(img1);
    imageLabel->resize(img1.width(), img1.height());
    //cout << img1.width() <<endl<< img1.height() << endl;
    ui->scrollArea->setWidgetResizable(1);
    ui->scrollArea->setWidget(imageLabel);
}

void MainWindow::on_pushButton_4_clicked() //生成六张度量结果的图
{
    QLabel *imageLabel = new QLabel(this);
    string env = "cd " + outDir.toStdString() + "\n source /etc/profile \n source ~/.bash_profile \n ";
    string mulutilpath = "$MULVALROOT/utils/";
    string cmd = "python " + mulutilpath + "topograph.py -g";
    string holeCmd = env + cmd;
    system(holeCmd.c_str());
    QSize picSize(540,405);
    QSize picSize2(400,300);
    QPixmap img;
    QPixmap img1;
    QPixmap img2;
    QPixmap img3;
    QPixmap img4;
    QPixmap img5;
    QPixmap img6;
    img1.load(outDir + "/3dresult.png");
    img2.load(outDir + "/h5v1s5detail.png");
    img3.load(outDir + "/h5v1s5network.png");
    img4.load(outDir + "/h5v1s5resource.png");
    img5.load(outDir + "/h5v1s5configuration.png");
    img6.load(outDir + "/h5v1s5performance.png");
    img1 = img1.scaled(picSize, Qt::KeepAspectRatio, Qt::SmoothTransformation); //用qsize把图片保持比例
    img2 = img2.scaled(picSize, Qt::KeepAspectRatio, Qt::SmoothTransformation);
    img3 = img3.scaled(picSize2, Qt::KeepAspectRatio, Qt::SmoothTransformation);
    img4 = img4.scaled(picSize2, Qt::KeepAspectRatio, Qt::SmoothTransformation);
    img5 = img5.scaled(picSize2, Qt::KeepAspectRatio, Qt::SmoothTransformation);
    img6 = img6.scaled(picSize2, Qt::KeepAspectRatio, Qt::SmoothTransformation);
    ui->label->setPixmap(img1);
    ui->label_2->setPixmap(img2);
    ui->label_3->setPixmap(img3);
    ui->label_4->setPixmap(img4);
    ui->label_5->setPixmap(img5);
    ui->label_6->setPixmap(img6);
    //img1.load(outDir + "/TopoAttackGraph.png");
    //imageLabel->setPixmap(img1);
    //imageLabel->resize(img1.width(), img1.height());
    //cout << img1.width() <<endl<< img1.height() << endl;
    //ui->scrollArea->setWidgetResizable(1);
    //ui->scrollArea->setWidget(imageLabel);
}

QPixmap MainWindow::scaleScroll(QPixmap p) //scroll的调整
{
    if((double)p.width() / (double)ui->scrollArea->width() < (double)p.height() / (double)ui->scrollArea->height()) //自适应大小，找最接近的是长还是宽
    {
        p = p.scaledToWidth(ui->scrollArea->width(), Qt::SmoothTransformation);
    }
    else
    {
        p = p.scaledToHeight(ui->scrollArea->height(), Qt::SmoothTransformation);
    }
    return p;
}
