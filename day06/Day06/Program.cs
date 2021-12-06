using System.Collections.Generic;
using System.Linq;

namespace Day06
{
    /// <summary>
    /// Slow implementation of Lanternfishes.
    /// </summary>
    class Lanternfishes
    {
        private IEnumerable<int> state;
        private readonly int age;
        private readonly int ageNew;

        public Lanternfishes(IEnumerable<int> state, int age, int ageNew)
        {
            this.state = state;
            this.age = age;
            this.ageNew = ageNew;
        }

        public void Advance()
        {
            state = state.Select(i => i - 1);
            var numNew = state.Count(i => i == -1);
            state = state.Select(i => i == -1 ? age : i);
            for (int i = 0; i < numNew; i++)
            {
                state = state.Append(ageNew);
            }
        }

        public void Advance(int n)
        {
            for (int i = 0; i < n; i++)
            {
                Advance();
            }
        }

        public int Count()
        {
            return state.Count();
        }

        public IEnumerable<int> State()
        {
            return state;
        }
    }

    /// <summary>
    /// Fast implementation of Lanternfishes.
    /// Unfortunately it's hard to guess from part 1 
    /// if individual fish data will be needed for part 2.
    /// </summary>
    class SmartLanternfishes
    {
        private IList<long> state;
        private readonly int age;
        private readonly int ageNew;

        public SmartLanternfishes(IEnumerable<int> state, int age, int ageNew)
        {
            this.state = new List<long>(ageNew + 1);
            for (int i = 0; i <= ageNew; i++)
            {
                this.state.Add(default);
            }
            this.age = age;
            this.ageNew = ageNew;
            foreach (var s in state)
            {
                this.state[s] += 1;
            }
        }

        public void Advance()
        {
            // read current count of 0 internal counter
            var atZero = state[0];
            // decrement by one
            this.state = state.Skip(1).Append(0).ToList();
            // reset decremented to age
            this.state[age] += atZero;
            // create new
            this.state[ageNew] += atZero;
        }
        public void Advance(int n)
        {
            for (int i = 0; i < n; i++)
            {
                Advance();
            }
        }

        public long Count()
        {
            return state.Sum();
        }


    }

    class Program
    {
        static void Main()
        {
            var example = new[] { 3, 4, 3, 1, 2 };
            var exampleSolution = new Lanternfishes(example, 6, 8);
            exampleSolution.Advance(18);
            System.Console.WriteLine("Example solution: {0}", exampleSolution.Count());
            var input = new[] {
                2, 1, 2, 1, 5, 1, 5, 1, 2, 2, 1, 1, 5, 1, 4, 4, 4, 3, 1, 2,
                2, 3, 4, 1, 1, 5, 1, 1, 4, 2, 5, 5, 5, 1, 1, 4, 5, 4, 1, 1,
                4, 2, 1, 4, 1, 2, 2, 5, 1, 1, 5, 1, 1, 3, 4, 4, 1, 2, 3, 1,
                5, 5, 4, 1, 4, 1, 2, 1, 5, 1, 1, 1, 3, 4, 1, 1, 5, 1, 5, 1,
                1, 5, 1, 1, 4, 3, 2, 4, 1, 4, 1, 5, 3, 3, 1, 5, 1, 3, 1, 1,
                4, 1, 4, 5, 2, 3, 1, 1, 1, 1, 3, 1, 2, 1, 5, 1, 1, 5, 1, 1,
                1, 1, 4, 1, 4, 3, 1, 5, 1, 1, 5, 4, 4, 2, 1, 4, 5, 1, 1, 3,
                3, 1, 1, 4, 2, 5, 5, 2, 4, 1, 4, 5, 4, 5, 3, 1, 4, 1, 5, 2,
                4, 5, 3, 1, 3, 2, 4, 5, 4, 4, 1, 5, 1, 5, 1, 2, 2, 1, 4, 1,
                1, 4, 2, 2, 2, 4, 1, 1, 5, 3, 1, 1, 5, 4, 4, 1, 5, 1, 3, 1,
                3, 2, 2, 1, 1, 4, 1, 4, 1, 2, 2, 1, 1, 3, 5, 1, 2, 1, 3, 1,
                4, 5, 1, 3, 4, 1, 1, 1, 1, 4, 3, 3, 4, 5, 1, 1, 1, 1, 1, 2,
                4, 5, 3, 4, 2, 1, 1, 1, 3, 3, 1, 4, 1, 1, 4, 2, 1, 5, 1, 1,
                2, 3, 4, 2, 5, 1, 1, 1, 5, 1, 1, 4, 1, 2, 4, 1, 1, 2, 4, 3,
                4, 2, 3, 1, 1, 2, 1, 5, 4, 2, 3, 5, 1, 2, 3, 1, 2, 2, 1, 4
            };
            var part1Solution = new SmartLanternfishes(input, 6, 8);
            part1Solution.Advance(80);
            System.Console.WriteLine("Part 1 solution: {0}", part1Solution.Count());
            var exampleSolution2 = new SmartLanternfishes(example, 6, 8);
            exampleSolution2.Advance(18);
            System.Console.WriteLine("Example solution 2: {0}", exampleSolution2.Count());
            var part2Solution = new SmartLanternfishes(input, 6, 8);
            part2Solution.Advance(256);
            System.Console.WriteLine("Part 2 solution: {0}", part2Solution.Count());
        }
    }
}
