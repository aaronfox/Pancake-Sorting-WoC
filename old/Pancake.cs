using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace PancakeFlip
{
    class Pancake
    {
        public int FitnessFunction(List<int> calcFitness)
        {
            int num = 0;

            for(int i = 0; i < calcFitness.Count -1; i++)
            {
                //if the size of next pancake is bigger than pancake current, 
                //increment number by 1. The higher the number, the worse the 
                //fitness is
                if(calcFitness[i] > calcFitness[i+1])
                {
                    num++;
                }
            }
            return num;
        }


        //read data from text file
        public List<int> ReadFile()
        {

            List<int> intOrder = new List<int>();

            string path = "https://raw.githubusercontent.com/aaronfox/Pancake-Sorting-WoC/master/PancakeData.txt";  //file path
            var fileStream = new FileStream(path, FileMode.Open, FileAccess.Read);
            using (var streamReader = new StreamReader(fileStream, Encoding.UTF8))
            {
                string line;
                while ((line = streamReader.ReadLine()) != null)
                {

                    intOrder.Add(Convert.ToInt32(line));
                }
            }
            return intOrder;
        }
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Pancake pc = new Pancake();

            List<int> data = pc.ReadFile();

            foreach (var i in data)
            {
                Console.WriteLine(i);
            }

            //Application.EnableVisualStyles();
            //Application.SetCompatibleTextRenderingDefault(false);
           // Application.Run(new Form1());
        }
    }
}
